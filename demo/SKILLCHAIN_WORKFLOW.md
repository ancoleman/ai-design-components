# Skill Chaining Workflow System

**A guided workflow that helps Claude trigger the right skills in the right order based on user goals.**

---

## How This Works

1. **User states a goal** → "I want to build a sales dashboard"
2. **Claude identifies required skills** → Based on keywords in the goal
3. **Claude triggers skills in order** → Each skill is actually invoked via `Skill` tool
4. **User makes choices** → Based on options each skill provides
5. **Skills chain together** → Output builds on previous skill outputs

---

## Keyword Trigger Mappings

### Primary Goal Keywords → Initial Skill Chain

| User Says | Triggers | Skill Chain Order |
|-----------|----------|-------------------|
| "dashboard", "analytics", "metrics" | Full dashboard workflow | theming → layouts → visualizing-data → tables → forms |
| "chart", "graph", "visualize", "plot" | Data viz workflow | theming → visualizing-data |
| "form", "input", "login", "signup", "register" | Form workflow | theming → building-forms → providing-feedback |
| "table", "grid", "list", "records" | Table workflow | theming → building-tables → search-filter |
| "theme", "colors", "brand", "styling" | Theming workflow | theming-components only |
| "layout", "structure", "responsive", "grid" | Layout workflow | theming → designing-layouts |
| "chat", "AI", "assistant", "conversation" | AI chat workflow | theming → building-ai-chat → forms |
| "onboarding", "tutorial", "guide", "help" | Onboarding workflow | theming → guiding-users |
| "notifications", "alerts", "toast", "feedback" | Feedback workflow | theming → providing-feedback |
| "upload", "files", "images", "media" | Media workflow | theming → managing-media → forms |
| "drag", "drop", "reorder", "sortable" | Drag-drop workflow | theming → implementing-drag-drop |
| "search", "filter", "find" | Search workflow | theming → implementing-search-filter |
| "navigation", "menu", "tabs", "routing" | Navigation workflow | theming → implementing-navigation |
| "timeline", "activity", "history", "feed" | Timeline workflow | theming → displaying-timelines |

---

## Skill Order of Operations

### Rule 1: Theming Always First
`theming-components` is the **hub** - invoke it first for any visual component work.

### Rule 2: Structure Before Content
`designing-layouts` comes before content skills (charts, tables, forms).

### Rule 3: Data Display Before Interaction
`visualizing-data` and `building-tables` before `building-forms` (filters).

### Rule 4: Feedback Last
`providing-feedback` comes last (loading states, success/error messages).

---

## Workflow Templates

### Template 1: Dashboard Workflow

**Trigger keywords:** "dashboard", "analytics", "metrics", "KPIs", "reports"

**Order of operations:**

```
Step 1: theming-components
├── Ask: "What's your brand color?" or "Light/dark theme preference?"
├── Output: Design tokens established
└── Keywords for next: layout, structure

Step 2: designing-layouts
├── Ask: "How many columns?" "Sidebar needed?" "Responsive breakpoints?"
├── Output: Layout grid defined
└── Keywords for next: charts, data, visualize

Step 3: visualizing-data
├── Ask: "What metrics?" "Time-based?" "Comparison or trend?"
├── Output: Chart types selected (bar, line, pie, etc.)
├── Decision tree:
│   ├── Comparing categories → Bar chart
│   ├── Showing trends → Line chart
│   ├── Part of whole → Pie chart (max 6 slices)
│   └── Distribution → Histogram
└── Keywords for next: table, details, records

Step 4: building-tables (if needed)
├── Ask: "Need detailed records?" "Sortable?" "Pagination?"
├── Output: Table configuration
└── Keywords for next: filter, search, controls

Step 5: building-forms
├── Ask: "What filters?" "Date range?" "Category selector?"
├── Output: Filter controls
└── Keywords for next: loading, notifications

Step 6: providing-feedback
├── Ask: "Loading states?" "Success messages?" "Error handling?"
├── Output: Feedback patterns
└── Complete
```

---

### Template 2: Form Workflow

**Trigger keywords:** "form", "login", "signup", "register", "input", "validation"

**Order of operations:**

```
Step 1: theming-components
├── Ask: "Brand colors for buttons/inputs?"
└── Output: Form styling tokens

Step 2: building-forms
├── Ask: "What data collecting?" "Validation needs?" "Multi-step?"
├── Decision tree:
│   ├── Short text → Text input
│   ├── Email → Email input with validation
│   ├── Password → Password input with strength meter
│   ├── Selection (2-7 options) → Radio group
│   ├── Selection (>7 options) → Select dropdown
│   ├── Multiple selection → Checkbox group
│   └── Date → Date picker
└── Output: Form structure

Step 3: providing-feedback
├── Ask: "Inline validation?" "Toast on submit?" "Error display?"
└── Output: Validation UX
```

---

### Template 3: Data Visualization Workflow

**Trigger keywords:** "chart", "graph", "visualize", "plot", "data viz"

**Order of operations:**

```
Step 1: theming-components
├── Ask: "Color palette preference?" "Colorblind-safe needed?"
└── Output: Chart color tokens (IBM palette recommended)

Step 2: visualizing-data
├── Ask: "What type of data?" "What story to tell?"
├── Decision tree:
│   ├── Categorical data
│   │   ├── Compare values → Bar Chart
│   │   ├── Show composition → Treemap or Pie (<6 slices)
│   │   └── Show flow → Sankey Diagram
│   ├── Continuous data
│   │   ├── Single variable → Histogram
│   │   └── Two variables → Scatter Plot
│   ├── Temporal data
│   │   ├── Single metric → Line Chart
│   │   ├── Multiple metrics → Small Multiples
│   │   └── Daily patterns → Calendar Heatmap
│   └── Hierarchical data
│       ├── Proportions → Treemap
│       └── Show depth → Sunburst
└── Output: Chart implementation with Recharts/D3
```

---

## Guided Prompts for Each Step

### After theming-components:
```
"I've established your design tokens. Now let's define the structure.

What layout do you need?
A) Single column (simple, mobile-first)
B) Two columns (sidebar + main)
C) Grid of cards/widgets
D) Complex dashboard (header, sidebar, main area)

Say 'layout [A/B/C/D]' to continue."
```

### After designing-layouts:
```
"Layout is set. Now let's add your data visualizations.

What metrics are you displaying?
- Revenue/sales over time? → I'll suggest line/bar charts
- Category comparisons? → I'll suggest bar charts
- Part of whole? → I'll suggest pie/treemap
- Correlations? → I'll suggest scatter plots

Describe your data and I'll invoke the visualizing-data skill."
```

### After visualizing-data:
```
"Charts are configured. Do you need:

A) A data table showing detailed records
B) Filter controls to slice the data
C) Both table and filters
D) Neither - charts are sufficient

Say 'next [A/B/C/D]' to continue."
```

### After building-tables:
```
"Table is set up. Now let's add interactivity.

What filter controls do you need?
- Date range picker
- Category dropdown
- Search box
- Multi-select tags

Describe your filter needs and I'll invoke the building-forms skill."
```

### After building-forms:
```
"Filters are ready. Final step - user feedback.

Do you want:
A) Loading spinners while data fetches
B) Toast notifications on actions
C) Inline validation messages
D) All of the above

Say 'feedback [A/B/C/D]' to complete the workflow."
```

---

## Claude's Internal Checklist

When user states a goal, Claude should:

1. **Parse keywords** → Map to skill chain template
2. **Announce the plan** → "I'll guide you through X skills in this order: ..."
3. **Invoke first skill** → `Skill(theming-components)`
4. **Ask qualifying questions** → Based on skill's decision tree
5. **Apply user choices** → Generate output using skill guidance
6. **Prompt for next step** → Guide to next skill in chain
7. **Repeat** → Until workflow complete

---

## Example Session

**User:** "I want to build a sales analytics dashboard with monthly revenue data"

**Claude:**
```
I'll help you build that dashboard. Based on your goal, I'll guide you through these skills in order:

1. theming-components → Establish colors and styling
2. designing-layouts → Set up dashboard structure
3. visualizing-data → Create revenue charts
4. building-forms → Add date/category filters

Let's start with theming.

[Invokes: Skill(theming-components)]

Based on the theming skill, I need to know:
- Do you have a brand color? (e.g., "#3B82F6" for blue)
- Light mode, dark mode, or both?
- Any accessibility requirements? (high contrast mode)
```

**User:** "Use blue #3B82F6, support both light and dark mode"

**Claude:**
```
Got it. Design tokens established with:
- Primary: #3B82F6 (blue)
- Light/dark theme support
- IBM colorblind-safe chart palette

Now let's set up your layout.

[Invokes: Skill(designing-layouts)]

For a sales dashboard, I recommend a responsive grid. Choose your structure:
A) Header + 3-column card grid (classic dashboard)
B) Sidebar navigation + main content area
C) Full-width with stacked sections

Which layout? Say 'layout A', 'layout B', or 'layout C'.
```

**User:** "layout A"

**Claude:**
```
Perfect. 3-column responsive grid with header.

Now let's visualize your revenue data.

[Invokes: Skill(visualizing-data)]

You mentioned monthly revenue. The visualizing-data skill recommends:
- Monthly trend → Line Chart or Bar Chart
- Year-over-year comparison → Grouped Bar Chart
- Revenue by category → Stacked Bar or Treemap

What story does your data tell?
A) Show revenue trend over 12 months → Line Chart
B) Compare months side by side → Bar Chart
C) Break down by product/region → Stacked Bar
D) Multiple metrics (revenue, expenses, profit) → Multi-line Chart
```

**User:** "D - I have revenue, expenses, and profit"

**Claude:**
```
Multi-metric chart selected. I'll create:
- Multi-line chart with 3 series (revenue, expenses, profit)
- Using chart tokens: --chart-color-1, --chart-color-2, --chart-color-3
- Responsive container, accessible tooltips

Do you also want summary stat cards showing totals?

[Continues through remaining skills...]
```

---

## Skill Invocation Syntax

When Claude needs to trigger a skill:

```
[Invokes: Skill(skill-name)]
```

Actual tool call:
```
Skill({ skill: "ui-data-skills:visualizing-data" })
```

Available skills in the plugin:
- `ui-data-skills:theming-components`
- `ui-data-skills:visualizing-data`
- `ui-data-skills:building-forms`
- `ui-data-skills:building-tables`
- `ui-data-skills:creating-dashboards`
- `ui-data-skills:providing-feedback`
- `ui-data-skills:implementing-navigation`
- `ui-data-skills:implementing-search-filter`
- `ui-data-skills:designing-layouts`
- `ui-data-skills:managing-media`
- `ui-data-skills:displaying-timelines`
- `ui-data-skills:building-ai-chat`
- `ui-data-skills:implementing-drag-drop`
- `ui-data-skills:guiding-users`

---

## Output Format

After completing a skill chain, Claude produces:

1. **Design tokens CSS** (from theming-components)
2. **Layout structure** (from designing-layouts)
3. **Component code** (from relevant skills)
4. **Integration notes** (how pieces connect)

All code uses CSS variables from design tokens for consistent theming.

---

## Demo Usage

To demo this system:

1. Start fresh Claude Code session with plugins installed
2. User says: "I want to build [goal]"
3. Claude parses keywords, announces skill chain
4. Claude invokes first skill, asks questions
5. User answers, Claude applies and moves to next skill
6. Repeat until complete
7. Final output: working themed component code

**The key insight:** Skills are actually triggered, not mimicked. Each skill brings its full decision tree and patterns into context.
