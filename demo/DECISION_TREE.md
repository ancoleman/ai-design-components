# Skill Chain Decision Tree

**Visual decision tree for determining skill order and choices within each skill.**

---

## Master Decision Tree

```
USER GOAL
    │
    ├─── Contains "dashboard", "analytics", "metrics", "admin"?
    │    └─── YES → DASHBOARD WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              ├── 2. Skill(designing-layouts)
    │              ├── 3. Skill(visualizing-data)
    │              ├── 4. Skill(building-tables) [if detailed data needed]
    │              ├── 5. Skill(building-forms) [for filters]
    │              └── 6. Skill(providing-feedback)
    │
    ├─── Contains "chart", "graph", "visualize", "plot"?
    │    └─── YES → VISUALIZATION WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              └── 2. Skill(visualizing-data)
    │
    ├─── Contains "form", "login", "signup", "input"?
    │    └─── YES → FORM WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              ├── 2. Skill(building-forms)
    │              └── 3. Skill(providing-feedback)
    │
    ├─── Contains "table", "grid", "records", "list"?
    │    └─── YES → TABLE WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              ├── 2. Skill(building-tables)
    │              └── 3. Skill(implementing-search-filter) [if searchable]
    │
    ├─── Contains "chat", "AI", "assistant", "conversation"?
    │    └─── YES → AI CHAT WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              ├── 2. Skill(building-ai-chat)
    │              └── 3. Skill(building-forms) [for input]
    │
    ├─── Contains "upload", "media", "gallery", "files"?
    │    └─── YES → MEDIA WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              └── 2. Skill(managing-media)
    │
    ├─── Contains "onboarding", "tutorial", "guide", "tour"?
    │    └─── YES → ONBOARDING WORKFLOW
    │              ├── 1. Skill(theming-components)
    │              └── 2. Skill(guiding-users)
    │
    └─── Contains "theme", "colors", "styling" ONLY?
         └─── YES → THEMING ONLY
                   └── 1. Skill(theming-components)
```

---

## Within-Skill Decision Trees

### theming-components Decision Tree

```
THEMING START
    │
    ├─── User has brand color?
    │    ├── YES → Generate 9-shade palette from base
    │    └── NO → Use default blue (#3B82F6)
    │
    ├─── Theme modes needed?
    │    ├── Light only → Single theme
    │    ├── Light + Dark → Two themes with data-theme attribute
    │    └── + High Contrast → Three themes (accessibility)
    │
    ├─── Special requirements?
    │    ├── RTL support → Use CSS logical properties
    │    ├── Reduced motion → Add motion token overrides
    │    └── Custom fonts → Define typography tokens
    │
    └─── OUTPUT: CSS variables file with all tokens
```

---

### visualizing-data Decision Tree

```
DATA VIZ START
    │
    ├─── What type of data?
    │    │
    │    ├─── CATEGORICAL (categories/groups)
    │    │    ├── Compare values? → Bar Chart
    │    │    ├── Show composition?
    │    │    │    ├── <6 categories → Pie Chart
    │    │    │    └── ≥6 categories → Treemap
    │    │    └── Show flow between? → Sankey Diagram
    │    │
    │    ├─── CONTINUOUS (numbers)
    │    │    ├── Single variable? → Histogram or Violin Plot
    │    │    └── Two variables? → Scatter Plot or Bubble Chart
    │    │
    │    ├─── TEMPORAL (time series)
    │    │    ├── Single metric? → Line Chart
    │    │    ├── Multiple metrics?
    │    │    │    ├── Compare trends → Multi-line Chart
    │    │    │    └── Cumulative → Stacked Area Chart
    │    │    └── Daily patterns? → Calendar Heatmap
    │    │
    │    └─── HIERARCHICAL (nested)
    │         ├── Show proportions? → Treemap
    │         └── Show depth/levels? → Sunburst or Dendrogram
    │
    ├─── How many data points?
    │    ├── <1,000 → SVG rendering (Recharts)
    │    ├── 1K-10K → Sample or aggregate
    │    └── >10K → Canvas rendering or server-side aggregation
    │
    ├─── Accessibility needs?
    │    ├── Colorblind safe → IBM palette (--chart-color-1 through 5)
    │    ├── Screen reader → Add aria-label descriptions
    │    └── Keyboard → Focusable data points
    │
    └─── OUTPUT: Chart component with token-based styling
```

---

### building-forms Decision Tree

```
FORMS START
    │
    ├─── What data to collect?
    │    │
    │    ├─── TEXT DATA
    │    │    ├── Short (<100 chars)
    │    │    │    ├── Email → Email input + validation
    │    │    │    ├── Password → Password input + strength meter
    │    │    │    ├── Phone → Tel input + formatting
    │    │    │    └── General → Text input
    │    │    └── Long (>100 chars) → Textarea
    │    │
    │    ├─── NUMERIC DATA
    │    │    ├── Integer → Number input with step
    │    │    ├── Currency → Currency input with symbol
    │    │    └── Range → Slider component
    │    │
    │    ├─── DATE/TIME
    │    │    ├── Date only → Date picker
    │    │    ├── Time only → Time picker
    │    │    ├── Date + Time → DateTime picker
    │    │    └── Date range → Date range picker
    │    │
    │    ├─── SELECTION
    │    │    ├── Yes/No → Checkbox or Toggle
    │    │    ├── One of few (2-7) → Radio group
    │    │    ├── One of many (>7) → Select dropdown
    │    │    ├── One of very many (>15) → Autocomplete
    │    │    └── Multiple choices → Checkbox group or Multi-select
    │    │
    │    └─── FILES
    │         ├── Single file → File input
    │         └── Multiple/drag-drop → File uploader component
    │
    ├─── Validation timing?
    │    ├── Simple form → On submit
    │    ├── Standard form → On blur (RECOMMENDED)
    │    ├── Real-time feedback → On change (debounced)
    │    └── Complex form → Progressive (blur → change after error)
    │
    ├─── Form structure?
    │    ├── Single page → Standard form
    │    ├── Multi-step → Wizard with progress
    │    └── Conditional → Dynamic fields based on answers
    │
    └─── OUTPUT: Form component with validation
```

---

### building-tables Decision Tree

```
TABLES START
    │
    ├─── Data volume?
    │    ├── <100 rows → Simple HTML table
    │    ├── 100-1K rows → Client-side pagination
    │    ├── 1K-10K rows → Virtual scrolling
    │    └── >10K rows → Server-side pagination + search
    │
    ├─── Features needed?
    │    ├── Sorting → Sortable columns
    │    ├── Filtering → Column filters or global search
    │    ├── Selection → Row checkboxes
    │    ├── Inline editing → Editable cells
    │    └── Export → CSV/Excel download
    │
    ├─── Column types?
    │    ├── Text → Standard cell
    │    ├── Number → Right-aligned, formatted
    │    ├── Date → Formatted date string
    │    ├── Status → Badge/chip component
    │    ├── Actions → Button column
    │    └── Sparkline → Inline mini chart
    │
    └─── OUTPUT: Table component with features
```

---

### implementing-search-filter Decision Tree

```
SEARCH/FILTER START
    │
    ├─── Search type?
    │    ├── Simple text → Search input with debounce
    │    ├── Autocomplete → Typeahead with suggestions
    │    └── Faceted → Multiple filter dimensions
    │
    ├─── Filter types needed?
    │    ├── Text match → Search input
    │    ├── Category → Dropdown or checkbox group
    │    ├── Range → Slider or min/max inputs
    │    ├── Date range → Date range picker
    │    └── Boolean → Toggle or checkbox
    │
    ├─── Filter behavior?
    │    ├── Apply button → Explicit apply
    │    └── Auto-apply → Filter on change (debounced)
    │
    └─── OUTPUT: Search/filter controls
```

---

### providing-feedback Decision Tree

```
FEEDBACK START
    │
    ├─── Feedback type?
    │    │
    │    ├─── LOADING STATES
    │    │    ├── Full page → Spinner overlay
    │    │    ├── Component → Skeleton loader
    │    │    ├── Button → Button loading state
    │    │    └── Progress → Progress bar
    │    │
    │    ├─── NOTIFICATIONS
    │    │    ├── Transient (auto-dismiss) → Toast
    │    │    ├── Requires action → Alert dialog
    │    │    ├── Inline → Alert banner
    │    │    └── System-level → Notification center
    │    │
    │    ├─── VALIDATION FEEDBACK
    │    │    ├── Field-level → Inline error/success
    │    │    ├── Form-level → Error summary
    │    │    └── Real-time → Live validation indicators
    │    │
    │    └─── EMPTY STATES
    │         ├── No data → Empty state illustration
    │         ├── No results → "No matches" message
    │         └── Error → Error state with retry
    │
    └─── OUTPUT: Feedback components
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL CHAIN QUICK REF                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ALWAYS START: theming-components                           │
│                                                             │
│  THEN BY GOAL:                                              │
│  ┌─────────────┬──────────────────────────────────────────┐│
│  │ Dashboard   │ layouts → data-viz → tables → forms      ││
│  │ Charts      │ data-viz                                 ││
│  │ Forms       │ forms → feedback                         ││
│  │ Tables      │ tables → search-filter                   ││
│  │ Chat        │ ai-chat → forms                          ││
│  │ Media       │ media                                    ││
│  │ Onboarding  │ guiding-users                            ││
│  └─────────────┴──────────────────────────────────────────┘│
│                                                             │
│  ALWAYS END: providing-feedback (if interactive)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Prompt Templates for Each Decision Point

### At data type decision:
```
"What kind of data are you working with?
A) Categories (products, regions, departments)
B) Numbers (revenue, counts, percentages)
C) Time series (daily, monthly, yearly trends)
D) Hierarchical (org chart, file tree, nested categories)"
```

### At chart type decision:
```
"What story does your data tell?
A) Comparing values across categories → Bar Chart
B) Showing change over time → Line Chart
C) Displaying parts of a whole → Pie/Treemap
D) Finding relationships → Scatter Plot"
```

### At form input decision:
```
"What information are you collecting?
A) Text (name, email, comments)
B) Selections (categories, options, yes/no)
C) Dates or times
D) Files or media"
```

### At table feature decision:
```
"What table features do you need?
A) Just display data (read-only)
B) Sortable columns
C) Searchable/filterable
D) Editable cells
E) All of the above"
```
