# Dashboard Blueprint

**Version:** 2.0.0
**Last Updated:** 2024-12-02
**Category:** Frontend

---

## Overview

Pre-configured skill chain optimized for building analytics dashboards, admin panels, KPI displays, and data-driven overview interfaces. This blueprint provides production-ready defaults for the most common dashboard patterns, minimizing configuration while maximizing quality.

---

## Trigger Keywords

**Primary (high confidence):**
- dashboard
- analytics
- admin panel
- metrics
- KPI
- overview

**Secondary (medium confidence):**
- admin
- stats
- monitoring
- business intelligence
- reporting
- insights

**Example goals that match:**
- "sales dashboard with charts"
- "analytics dashboard for user metrics"
- "admin dashboard with real-time data"
- "KPI overview page"
- "executive dashboard showing revenue trends"
- "monitoring dashboard with graphs and tables"

---

## Skill Chain (Pre-configured)

This blueprint invokes 7 skills in the following order:

```
1. theming-components          (foundation - always required)
2. designing-layouts            (grid system for dashboard layout)
3. creating-dashboards          (core dashboard components)
4. visualizing-data             (charts and graphs)
5. building-tables              (optional - data grid display)
6. providing-feedback           (loading states, notifications)
7. assembling-components        (final assembly - always required)
```

**Total estimated time:** 25-35 minutes
**Total estimated questions:** 8-12 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. theming-components
```yaml
color_scheme: "corporate-blue"
  # Professional blue-gray palette optimized for data visualization
  # Primary: #3B82F6 (blue-500)
  # Success: #10B981 (green-500)
  # Warning: #F59E0B (amber-500)
  # Danger: #EF4444 (red-500)

theme_modes: ["light", "dark"]
  # Both light and dark modes for accessibility
  # Dark mode optimized for extended dashboard viewing

spacing_base: "8px"
  # 8px grid system for consistent component spacing
  # Scale: 4, 8, 12, 16, 24, 32, 48, 64px
```

### 2. designing-layouts
```yaml
system: "css-grid"
  # CSS Grid for flexible dashboard layouts
  # Supports responsive grid areas

layout: "sidebar-main"
  # Left sidebar navigation (240px)
  # Main content area (flexible)
  # Optional right panel for filters

responsive: true
  # Mobile: Stacked layout with collapsible sidebar
  # Tablet: 2-column grid
  # Desktop: Full sidebar-main layout

breakpoints: ["sm", "md", "lg", "xl"]
  # sm: 640px (mobile)
  # md: 768px (tablet)
  # lg: 1024px (desktop)
  # xl: 1280px (large desktop)
```

### 3. creating-dashboards
```yaml
layout: "sidebar-grid"
  # Sidebar navigation + grid-based dashboard content
  # Supports: Header, KPI cards row, chart grid, data table section

kpi_cards: 4
  # Four primary KPI cards in top row
  # Common metrics: Revenue, Users, Conversion, Growth
  # Auto-adjusts to 2 columns on tablet, 1 on mobile

responsive: true
  # Automatic reflowing of dashboard components
  # Touch-friendly on mobile devices
  # Optimized spacing for different screen sizes

auto_refresh: false
  # Set to true if real-time data updates needed
  # Polling interval: 30 seconds (customizable)

export_enabled: true
  # Enable PDF/CSV export buttons
  # Positioned in dashboard header
```

### 4. visualizing-data
```yaml
chart_types: ["line", "bar", "pie"]
  # Line charts: Trends over time
  # Bar charts: Comparisons between categories
  # Pie charts: Proportions and percentages

library: "recharts"
  # React-friendly, declarative API
  # Excellent for dashboards (optimized for responsive)
  # Built-in animations and tooltips

responsive: true
  # Charts automatically resize on viewport changes
  # Maintains aspect ratio
  # Readable on all screen sizes

theme_aware: true
  # Charts adapt to light/dark theme
  # Colors pulled from design tokens
  # Accessible contrast ratios

interactive: true
  # Hover tooltips for data points
  # Click interactions for drill-down (optional)
  # Zoom/pan for time-series (optional)

animations: "smooth"
  # Smooth transitions on data updates
  # Entry animations on initial render
  # Performance-optimized (requestAnimationFrame)
```

### 5. building-tables (optional)
```yaml
pagination: true
  # Default: 10 rows per page
  # Options: 10, 25, 50, 100

sorting: true
  # Click column headers to sort
  # Multi-column sorting with shift-click

filtering: true
  # Column-level filters
  # Search across all columns

row_selection: false
  # Set to true for batch actions
  # Checkbox column + select all

export_csv: true
  # Export current view to CSV
  # Respects active filters/sorting

virtual_scrolling: false
  # Enable for 1000+ rows
  # Renders only visible rows (performance)
```

### 6. providing-feedback
```yaml
toast_position: "top-right"
  # Non-intrusive notification placement
  # Auto-dismiss after 5 seconds
  # Stacks vertically for multiple toasts

loading_type: "skeleton"
  # Skeleton screens for dashboard components
  # Prevents layout shift
  # Shows structure while loading

error_handling: "toast"
  # API errors shown as toast notifications
  # Non-blocking, dismissible
  # Retry option for failed requests

success_messages: true
  # Confirm actions (e.g., "Data exported successfully")
  # Green checkmark icon
  # Auto-dismiss
```

### 7. assembling-components
```yaml
validate_tokens: true
  # Enforce token usage (no hardcoded values)
  # Validate all components reference tokens.css
  # Auto-fix common violations

production_ready: true
  # Include error boundaries
  # Add loading states for all async operations
  # Accessibility compliance (WCAG 2.1 AA)
  # TypeScript types included
  # PropTypes for component validation

file_structure: "feature-based"
  # /dashboard/components/ (KPI cards, charts)
  # /dashboard/layouts/ (grid layout)
  # /dashboard/hooks/ (data fetching)
  # /dashboard/utils/ (formatters, calculations)
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Dashboard Purpose
```
What metrics will your dashboard display?

Examples:
- Sales metrics (revenue, orders, conversion)
- User analytics (signups, activity, retention)
- System monitoring (uptime, errors, performance)
- Custom metrics

Your answer: _______________
```

**Why this matters:**
- Determines KPI card content
- Suggests appropriate chart types
- Influences data schema recommendations

**Default if skipped:** "General analytics (revenue, users, conversion, growth)"

---

### Question 2: Data Table Inclusion
```
Include a data table below the charts?

Options:
1. Yes - full-featured table with sorting/filtering (recommended for detailed data)
2. Yes - simple table without advanced features (faster implementation)
3. No - charts and KPIs only (cleaner interface)

Your answer: _______________
```

**Why this matters:**
- Determines if `building-tables` skill is invoked
- Affects layout grid structure
- Impacts bundle size (~15KB for table library)

**Default if skipped:** "Yes - full-featured table"

---

### Question 3: Advanced Features
```
Which additional features do you need? (select multiple)

Options:
a. Dark mode toggle (already included by default)
b. Real-time data updates (30-second polling)
c. Date range picker for filtering
d. Export to PDF/CSV
e. None of the above

Your answer (comma-separated, e.g., "b,c,d"): _______________
```

**Why this matters:**
- Real-time updates require additional state management
- Date picker adds ~10KB dependency
- Export functionality requires additional libraries

**Default if skipped:** "a,d" (dark mode + export)

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_dashboard_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "dashboard",
        "analytics dashboard",
        "admin panel",
        "kpi",
        "metrics",
        "overview"
    ])

    # Secondary keywords + data visualization
    secondary_match = (
        any(keyword in goal_lower for keyword in ["admin", "analytics", "stats", "monitoring"]) and
        any(keyword in goal_lower for keyword in ["chart", "graph", "data", "metrics"])
    )

    return primary_match or secondary_match
```

**Confidence levels:**
- **High (90%+):** Contains "dashboard" + data-related term
- **Medium (70-89%):** Contains "admin" or "analytics" + visualization term
- **Low (50-69%):** Contains "overview" + multiple metrics

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 📊 DASHBOARD BLUEPRINT DETECTED                            │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized Dashboard Blueprint!      │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Responsive sidebar + grid layout                       │
│  ✓ 4 KPI metric cards                                     │
│  ✓ Interactive charts (line, bar, pie)                    │
│  ✓ Data table with sorting/filtering                      │
│  ✓ Light/dark theme support                               │
│  ✓ Loading states + error handling                        │
│  ✓ Professional blue color scheme                         │
│                                                            │
│ Using blueprint reduces questions from 12 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~10 min)            │
│  2. Custom configuration (12 questions, ~30 min)          │
│  3. Skip all questions (use all defaults, ~5 min)         │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
dashboard-project/
├── src/
│   ├── tokens.css                      # Design tokens (ALWAYS FIRST)
│   │   # CSS custom properties for colors, spacing, typography
│   │   # Light and dark theme definitions
│   │
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── DashboardLayout.tsx     # Main dashboard container
│   │   │   ├── DashboardHeader.tsx     # Top header with title, filters, export
│   │   │   ├── KPICard.tsx             # Individual metric card component
│   │   │   ├── KPIGrid.tsx             # Grid container for KPI cards
│   │   │   ├── ChartGrid.tsx           # Grid container for charts
│   │   │   ├── DataTable.tsx           # Data table component (if included)
│   │   │   └── ThemeToggle.tsx         # Light/dark mode switch
│   │   │
│   │   ├── charts/
│   │   │   ├── LineChart.tsx           # Time-series line chart
│   │   │   ├── BarChart.tsx            # Category comparison bar chart
│   │   │   ├── PieChart.tsx            # Proportion pie chart
│   │   │   └── ChartContainer.tsx      # Wrapper with loading/error states
│   │   │
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx             # Navigation sidebar
│   │   │   ├── MainContent.tsx         # Main content wrapper
│   │   │   └── GridLayout.tsx          # Responsive grid system
│   │   │
│   │   └── feedback/
│   │       ├── Toast.tsx               # Notification toast
│   │       ├── ToastContainer.tsx      # Toast manager
│   │       ├── SkeletonLoader.tsx      # Loading skeleton
│   │       └── ErrorBoundary.tsx       # Error boundary wrapper
│   │
│   ├── hooks/
│   │   ├── useDashboardData.ts         # Data fetching hook
│   │   ├── useTheme.ts                 # Theme management hook
│   │   ├── useToast.ts                 # Toast notification hook
│   │   └── useExport.ts                # CSV/PDF export hook
│   │
│   ├── utils/
│   │   ├── formatters.ts               # Number/date formatting
│   │   ├── calculations.ts             # Metric calculations
│   │   └── exportHelpers.ts            # Export utility functions
│   │
│   ├── types/
│   │   ├── dashboard.ts                # Dashboard data types
│   │   ├── charts.ts                   # Chart configuration types
│   │   └── kpi.ts                      # KPI metric types
│   │
│   ├── data/
│   │   ├── mockData.ts                 # Sample dashboard data
│   │   └── api.ts                      # API integration layer
│   │
│   ├── App.tsx                         # Root application component
│   ├── main.tsx                        # Application entry point
│   └── index.css                       # Global styles (imports tokens.css)
│
├── public/
│   └── index.html                      # HTML template
│
├── package.json                        # Dependencies and scripts
├── tsconfig.json                       # TypeScript configuration
├── vite.config.ts                      # Vite build configuration
└── README.md                           # Setup and usage instructions
```

---

## Component Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                   DashboardLayout                       │
│  ┌───────────────────────────────────────────────────┐ │
│  │ useDashboardData() hook                           │ │
│  │  - Fetches metrics, chart data, table data        │ │
│  │  - Manages loading/error states                   │ │
│  │  - Auto-refresh (if enabled)                      │ │
│  └────────────────┬────────────────────────────────────┘ │
│                   │                                      │
│  ┌────────────────▼────────────────┐                    │
│  │ Sidebar          │  Main Content │                   │
│  │                  │               │                   │
│  │ - Navigation     │ ┌─────────────▼──────────────┐   │
│  │ - Theme Toggle   │ │ DashboardHeader            │   │
│  │                  │ │  - Title, filters, export  │   │
│  │                  │ └────────────────────────────┘   │
│  │                  │                                   │
│  │                  │ ┌────────────────────────────┐   │
│  │                  │ │ KPIGrid                    │   │
│  │                  │ │  - 4 KPICard components    │   │
│  │                  │ │  - Responsive grid layout  │   │
│  │                  │ └────────────────────────────┘   │
│  │                  │                                   │
│  │                  │ ┌────────────────────────────┐   │
│  │                  │ │ ChartGrid                  │   │
│  │                  │ │  - LineChart (trends)      │   │
│  │                  │ │  - BarChart (compare)      │   │
│  │                  │ │  - PieChart (proportions)  │   │
│  │                  │ └────────────────────────────┘   │
│  │                  │                                   │
│  │                  │ ┌────────────────────────────┐   │
│  │                  │ │ DataTable (if enabled)     │   │
│  │                  │ │  - Sortable columns        │   │
│  │                  │ │  - Filterable data         │   │
│  │                  │ │  - Pagination controls     │   │
│  │                  │ └────────────────────────────┘   │
│  └──────────────────┴───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

Toast Notifications (overlay)
Error Boundary (wrapper)
```

### Theme Integration

All components reference design tokens from `tokens.css`:

```css
/* Example component styles */
.kpi-card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
  box-shadow: var(--shadow-sm);
}

.kpi-value {
  color: var(--color-text-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
}

.kpi-label {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.kpi-change-positive {
  color: var(--color-success);
}

.kpi-change-negative {
  color: var(--color-danger);
}
```

**No hardcoded values allowed.** All visual properties must reference tokens.

---

## Default Metrics and Data

### KPI Cards (default 4)

```typescript
interface KPIMetric {
  id: string;
  label: string;
  value: string | number;
  change: number;           // Percentage change
  changeType: 'increase' | 'decrease';
  icon: string;
  format: 'currency' | 'number' | 'percentage';
}

const defaultKPIs: KPIMetric[] = [
  {
    id: 'revenue',
    label: 'Total Revenue',
    value: 124500,
    change: 12.5,
    changeType: 'increase',
    icon: 'dollar-sign',
    format: 'currency'
  },
  {
    id: 'users',
    label: 'Active Users',
    value: 8432,
    change: 8.2,
    changeType: 'increase',
    icon: 'users',
    format: 'number'
  },
  {
    id: 'conversion',
    label: 'Conversion Rate',
    value: 3.24,
    change: -0.5,
    changeType: 'decrease',
    icon: 'trending-up',
    format: 'percentage'
  },
  {
    id: 'growth',
    label: 'Month-over-Month Growth',
    value: 18.7,
    change: 4.3,
    changeType: 'increase',
    icon: 'bar-chart',
    format: 'percentage'
  }
];
```

### Chart Data (sample)

```typescript
// Line chart: Trend over time
const lineChartData = [
  { month: 'Jan', revenue: 98000, users: 7200 },
  { month: 'Feb', revenue: 105000, users: 7600 },
  { month: 'Mar', revenue: 112000, users: 7900 },
  { month: 'Apr', revenue: 118000, users: 8100 },
  { month: 'May', revenue: 121000, users: 8300 },
  { month: 'Jun', revenue: 124500, users: 8432 }
];

// Bar chart: Category comparison
const barChartData = [
  { category: 'Product A', sales: 45000 },
  { category: 'Product B', sales: 38000 },
  { category: 'Product C', sales: 25000 },
  { category: 'Product D', sales: 16500 }
];

// Pie chart: Proportions
const pieChartData = [
  { name: 'Direct', value: 42 },
  { name: 'Organic', value: 28 },
  { name: 'Referral', value: 18 },
  { name: 'Social', value: 12 }
];
```

---

## Dependencies

The blueprint includes these npm packages:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.0",              // Charts
    "date-fns": "^2.30.0",              // Date formatting
    "clsx": "^2.0.0"                    // Conditional classnames
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

**Optional dependencies** (based on answers):
- `react-table` (if full-featured table selected): ~50KB
- `react-datepicker` (if date range picker enabled): ~35KB
- `jspdf` + `jspdf-autotable` (if PDF export enabled): ~280KB
- `papaparse` (if CSV export enabled): ~45KB

---

## Accessibility Features

All components include:

- **Keyboard navigation:** Tab order, focus indicators, keyboard shortcuts
- **Screen reader support:** ARIA labels, roles, live regions
- **Color contrast:** WCAG 2.1 AA compliance (4.5:1 for text)
- **Semantic HTML:** Proper heading hierarchy, landmark regions
- **Focus management:** Trapped focus in modals, skip links
- **Reduced motion:** Respects `prefers-reduced-motion` media query

---

## Performance Optimizations

- **Code splitting:** Lazy load chart components
- **Memoization:** React.memo for expensive components
- **Virtual scrolling:** For tables with 1000+ rows
- **Debounced filtering:** Search input with 300ms debounce
- **Optimized re-renders:** useCallback, useMemo for data transformations
- **Image optimization:** Lazy loading, responsive images

---

## Testing Recommendations

Include these test files:

```
tests/
├── components/
│   ├── KPICard.test.tsx           # Unit tests for KPI card
│   ├── LineChart.test.tsx         # Chart rendering tests
│   └── DataTable.test.tsx         # Table functionality tests
│
├── hooks/
│   ├── useDashboardData.test.ts   # Data fetching hook tests
│   └── useTheme.test.ts           # Theme switching tests
│
└── integration/
    └── DashboardFlow.test.tsx     # End-to-end dashboard tests
```

**Test coverage targets:**
- Components: 80%+
- Hooks: 90%+
- Utils: 95%+

---

## Customization Points

After blueprint generation, users can easily customize:

1. **Color scheme:** Edit `tokens.css` color variables
2. **KPI metrics:** Modify `mockData.ts` with actual metrics
3. **Chart types:** Add/remove charts in `ChartGrid.tsx`
4. **Layout:** Adjust grid columns in `GridLayout.tsx`
5. **Sidebar navigation:** Update links in `Sidebar.tsx`
6. **Data source:** Replace mock data with API calls in `api.ts`

---

## Migration Path

If user starts with blueprint but needs custom features later:

1. **Add new chart type:** Run `/skillchain visualizing-data` again
2. **Add authentication:** Run `/skillchain auth-security`
3. **Add real-time updates:** Run `/skillchain realtime-sync`
4. **Add advanced filters:** Run `/skillchain implementing-search-filter`

All additions will integrate with existing token system and layout.

---

## Version History

**2.0.0** (2024-12-02)
- Initial dashboard blueprint
- 7-skill chain with optimized defaults
- 3-question quick configuration
- Corporate blue theme as default
- Recharts as default charting library
- Full accessibility support

---

## Related Blueprints

- **Form Blueprint:** For data entry dashboards
- **Table Blueprint:** For data-heavy admin interfaces
- **AI Chat Blueprint:** For conversational analytics
- **Monitoring Blueprint:** For real-time system metrics

---

**Blueprint Complete**
