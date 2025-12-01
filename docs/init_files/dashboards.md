# AI-Assisted Component Library: Dashboard Components
## Master Plan for Dashboard & Analytics Interface Skill

**Document Version:** 1.0
**Date:** November 13, 2025
**Purpose:** Comprehensive framework for building dashboard interfaces that combine data visualization, KPIs, real-time updates, and interactive analytics

---

## Executive Summary

Dashboards are composite interfaces combining multiple component types (visualizations, tables, forms, filters) into unified analytics experiences. This skill provides systematic guidance for dashboard architecture, layout patterns, real-time data handling, and creating effective business intelligence interfaces.

**Key Value:**
- Combines data-viz + tables + forms + filters into cohesive experiences
- Real-time data update patterns
- Dashboard layout and grid systems
- KPI card design and metric presentation
- Filter coordination across widgets
- Performance optimization for multi-widget displays

---

## Component Taxonomy

### Core Dashboard Elements

**KPI Cards**
- Big number display (primary metric)
- Trend indicator (↑↓ arrows, %, change)
- Sparkline (mini trend visualization)
- Time period selector
- Comparison value (vs last period)

**Widget Containers**
- Title bar with actions (refresh, export, settings)
- Loading states (skeleton, spinner)
- Error states (retry, configure)
- Resize handles
- Drag handles for rearrangement

**Dashboard Layouts**
- Grid system (12-column, responsive)
- Fixed dashboard (designer-defined layout)
- Customizable dashboard (user drag-to-arrange)
- Responsive breakpoints (desktop, tablet, mobile)

**Global Controls**
- Date range picker (affects all widgets)
- Filter panel (apply to multiple widgets)
- Refresh button/auto-refresh toggle
- Export dashboard (PDF, image)
- Settings/preferences

---

## Dashboard Architecture Patterns

### Pattern 1: Fixed Layout

**Characteristics:**
- Designer defines widget placement
- Optimized for specific use case
- Consistent experience across users
- Simpler implementation

**Best For:**
- Executive dashboards
- Public displays/TVs
- Embedded analytics
- Standardized reports

### Pattern 2: Customizable Grid

**Characteristics:**
- User can resize and rearrange widgets
- Drag-and-drop interface
- Save personal layouts
- Widget library/catalog

**Best For:**
- Power user tools
- Multi-tenant SaaS
- Personalized workspaces
- Analyst workbenches

### Pattern 3: Template-Based

**Characteristics:**
- Pre-built templates for common use cases
- Users start from template
- Can customize from there
- Library of templates

**Best For:**
- Onboarding new users
- Industry-specific dashboards
- Best practice patterns
- Faster time-to-value

---

## Real-Time Data Patterns

### WebSocket Updates

**Full Update:**
```javascript
// New data arrives
websocket.onmessage = (event) => {
  const newData = JSON.parse(event.data);
  updateAllWidgets(newData);
};
```

**Incremental Update:**
```javascript
// Only changed data sent
websocket.onmessage = (event) => {
  const { widgetId, delta } = JSON.parse(event.data);
  updateWidget(widgetId, delta);
};
```

### Polling Strategy

**Simple Polling:**
- Fixed interval (every 30s, 1m, 5m)
- All widgets refresh together
- Easy to implement
- Can be inefficient

**Smart Polling:**
- Different refresh rates per widget type
- Pause when tab inactive
- Exponential backoff on errors
- User-configurable intervals

### Server-Sent Events (SSE)

**Advantages:**
- Unidirectional (server → client)
- Auto-reconnect built-in
- Simple protocol
- Better for updates vs bidirectional chat

---

## KPI Card Design

### Essential Elements

```
┌────────────────────────────┐
│ Revenue (This Month)       │ ← Label
│                            │
│  $1,245,832               │ ← Primary metric
│  ↑ 15.3% vs last month    │ ← Trend indicator
│  ▂▃▅▆▇ (sparkline)        │ ← Mini trend
└────────────────────────────┘
```

### Best Practices

**Number Formatting:**
- Abbreviate large numbers (1.2M not 1,245,832)
- Consistent decimal places
- Currency symbols
- Percentage formatting
- Locale-aware (1,234.56 vs 1.234,56)

**Trend Indicators:**
- Use color sparingly (not always red=bad, green=good)
- Include direction arrow
- Show absolute and relative change
- Indicate time period clearly

**Sparklines:**
- 20-30 data points max
- Match time period of metric
- Light, non-distracting
- Clickable to see detail

---

## Filter Coordination

### Global Filters

**Problem:** User selects date range, should affect all widgets

**Implementation:**
```javascript
// Context for global filters
<DashboardContext.Provider value={{ filters, setFilters }}>
  <FilterPanel />
  <Widget1 />
  <Widget2 />
  <Widget3 />
</DashboardContext.Provider>

// Each widget subscribes to filters
function Widget1() {
  const { filters } = useDashboardContext();
  const data = useFetchData(filters);
  return <Chart data={data} />;
}
```

**Best Practices:**
- Show active filters prominently
- "Clear all filters" button
- Filter chips (individual removal)
- URL sync (shareable filtered dashboard)
- Preserve filters on navigation

---

## Performance Optimization

### Lazy Loading

**Pattern:**
- Render above-the-fold widgets first
- Lazy load below-the-fold
- Show skeleton/placeholder
- Load on scroll or after delay

### Widget Caching

**Strategy:**
- Cache widget data (with TTL)
- Serve from cache while fetching fresh
- Show "Updated X seconds ago"
- Manual refresh option

### Parallel Loading

**Approach:**
```javascript
// Load all widget data in parallel
const [kpis, chart1, chart2, table] = await Promise.all([
  fetchKPIs(),
  fetchChart1Data(),
  fetchChart2Data(),
  fetchTableData()
]);
```

---

## Responsive Dashboard Strategies

### Desktop (>1200px)
- 3-4 column grid
- Side-by-side widgets
- Rich tooltips
- Hover interactions

### Tablet (768px-1200px)
- 2 column grid
- Stacked layout
- Touch-friendly controls
- Simplified filters

### Mobile (<768px)
- Single column
- Vertical scrolling
- Prioritize KPIs
- Simplified visualizations
- Bottom sheet filters

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7). This ensures you're using the latest, most secure versions.

**Note:** The recommendations below were researched comprehensively in November 2025 and are production-ready. Validation is optional.

---

## Recommended Libraries & Tools

### Dashboard Component Libraries (2025)

#### **Primary: Tremor** (Built for Dashboards & Analytics)

**Library:** `/tremorlabs/tremor`
**Trust Score:** 7.4/10
**Code Snippets:** 1,281+ (Tremor Blocks)

**Why Tremor?**
- **Purpose-Built**: Specifically designed for dashboards and analytics
- **Built on Tailwind + Recharts**: Modern tech stack
- **Pre-Built Components**: KPI cards, charts, tables ready to use
- **35+ Components**: Comprehensive dashboard toolkit
- **Accessible**: Built on Radix UI primitives
- **TypeScript**: Full type safety

**When to Use:**
- Building analytics dashboards
- Need KPI cards and charts quickly
- Using Tailwind CSS
- Want polished, professional components out-of-box
- React projects

**Installation:**
```bash
npm install @tremor/react
```

**KPI Card Example:**
```tsx
import { Card, Metric, Text, Flex, BadgeDelta } from '@tremor/react';

function KPICard() {
  return (
    <Card>
      <Text>Total Revenue</Text>
      <Metric>$45,231.89</Metric>
      <Flex justifyContent="start" className="mt-4">
        <BadgeDelta deltaType="increase">↑ 12.5%</BadgeDelta>
        <Text className="ml-2">vs last month</Text>
      </Flex>
    </Card>
  );
}
```

**Dashboard with Charts:**
```tsx
import { Card, Title, BarChart, Grid } from '@tremor/react';

const salesData = [
  { month: 'Jan', sales: 2890, expenses: 2338 },
  { month: 'Feb', sales: 2756, expenses: 2103 },
  { month: 'Mar', sales: 3322, expenses: 2194 },
];

function Dashboard() {
  return (
    <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-4">
      <Card>
        <Title>Revenue</Title>
        <Metric>$71,465</Metric>
      </Card>

      <Card>
        <Title>Customers</Title>
        <Metric>1,234</Metric>
      </Card>

      <Card className="col-span-2">
        <Title>Sales vs Expenses</Title>
        <BarChart
          data={salesData}
          index="month"
          categories={["sales", "expenses"]}
          colors={["blue", "red"]}
          valueFormatter={(value) => `$${value.toLocaleString()}`}
        />
      </Card>
    </Grid>
  );
}
```

---

#### **Grid Layout: react-grid-layout** (Customizable Dashboards)

**Library:** `/react-grid-layout/react-grid-layout`
**Trust Score:** 6.7/10
**Code Snippets:** 33+

**Why react-grid-layout?**
- **Drag-and-Drop**: Users can rearrange widgets
- **Resizable**: Widgets can be resized
- **Responsive**: Breakpoint-based layouts
- **Persistent**: Save layouts to localStorage
- **Flexible**: Works with any component library

**When to Use:**
- Need customizable dashboards (user-configurable)
- Drag-to-rearrange widgets
- Different layouts per screen size
- Power user tools

**Installation:**
```bash
npm install react-grid-layout
```

**Responsive Dashboard Example:**
```tsx
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

function CustomizableDashboard() {
  const [layouts, setLayouts] = useState({
    lg: [
      { i: 'kpi1', x: 0, y: 0, w: 3, h: 2 },
      { i: 'kpi2', x: 3, y: 0, w: 3, h: 2 },
      { i: 'chart1', x: 0, y: 2, w: 6, h: 4 },
    ]
  });

  return (
    <ResponsiveGridLayout
      className="layout"
      layouts={layouts}
      breakpoints={{ lg: 1200, md: 996, sm: 768 }}
      cols={{ lg: 12, md: 10, sm: 6 }}
      rowHeight={60}
      onLayoutChange={(layout, layouts) => {
        setLayouts(layouts);
        localStorage.setItem('dashboardLayout', JSON.stringify(layouts));
      }}
    >
      <div key="kpi1">
        <KPICard title="Revenue" value="$45K" />
      </div>
      <div key="kpi2">
        <KPICard title="Users" value="1,234" />
      </div>
      <div key="chart1">
        <SalesChart />
      </div>
    </ResponsiveGridLayout>
  );
}
```

---

### Real-Time Data Updates

#### **WebSocket vs. Server-Sent Events (SSE)**

**Based on research:**

**Use WebSocket When:**
- Need bidirectional communication
- Real-time collaboration (multiple users)
- Chat features
- Gaming/live interactions

**Use SSE When:**
- Unidirectional updates (server → client)
- Dashboard metrics updates
- Live feeds (news, stocks, notifications)
- Simpler implementation needed

**SSE Recommended for Dashboards:**
```tsx
import { useEffect, useState } from 'react';

function useSSEMetrics(endpoint) {
  const [metrics, setMetrics] = useState({});

  useEffect(() => {
    const eventSource = new EventSource(endpoint);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data);
    };

    eventSource.onerror = () => {
      console.error('SSE connection error');
      eventSource.close();
    };

    return () => eventSource.close();
  }, [endpoint]);

  return metrics;
}

function LiveDashboard() {
  const metrics = useSSEMetrics('/api/metrics/stream');

  return (
    <div>
      <KPICard title="Active Users" value={metrics.activeUsers} />
      <KPICard title="Revenue" value={`$${metrics.revenue}`} />
    </div>
  );
}
```

**WebSocket Pattern (Bidirectional):**
```tsx
import { useEffect, useState } from 'react';

function useWebSocket(url) {
  const [data, setData] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket(url);

    websocket.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWs(websocket);

    return () => websocket.close();
  }, [url]);

  const sendMessage = (message) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  };

  return { data, sendMessage };
}
```

---

### Library Comparison Matrix

| Library | Use Case | Pre-Built Components | Customization | Bundle Size | Best For |
|---------|----------|---------------------|---------------|-------------|----------|
| **Tremor** | Dashboards | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Medium | Analytics dashboards |
| **react-grid-layout** | Grid System | ⭐ | ⭐⭐⭐⭐⭐ | Small | Customizable layouts |
| **Custom (data-viz + tables)** | Flexible | ⭐ | ⭐⭐⭐⭐⭐ | Variable | Maximum control |

---

### Recommendations by Use Case

**Analytics Dashboard (Quick) → Tremor**
- Pre-built KPI cards
- Charts included
- Professional appearance
- Minimal code

**Customizable Dashboard → react-grid-layout + Custom Components**
- User can rearrange widgets
- Fully flexible
- Combine with data-viz skill charts
- Maximum control

**Real-Time Monitoring → SSE + Recharts/Tremor**
- Server-Sent Events for data stream
- Auto-updating charts
- Simple implementation
- Unidirectional updates

**Collaborative Dashboard → WebSocket + react-grid-layout**
- Multi-user editing
- Real-time sync
- Bidirectional communication

---

### Implementation Recommendations

**Recommended Stack (Quick Dashboard):**
```bash
npm install @tremor/react
```
- Use Tremor for KPI cards, charts, tables
- Built-in responsive grid
- Professional out-of-box

**Recommended Stack (Custom Dashboard):**
```bash
npm install react-grid-layout recharts
```
- react-grid-layout for widget arrangement
- Recharts (from data-viz skill) for charts
- Custom KPI components with design tokens
- Maximum flexibility

---

## Styling & Theming

### Design Token Integration

All dashboard components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--dashboard-bg` - Dashboard background color
- `--widget-bg` - Widget/card background
- `--widget-border-color` - Widget borders
- `--kpi-value-color` - KPI number color
- `--kpi-label-color` - KPI label color
- `--kpi-trend-positive` - Positive trend indicator
- `--kpi-trend-negative` - Negative trend indicator
- `--kpi-trend-neutral` - Neutral trend color

**Spacing Tokens:**
- `--dashboard-padding` - Dashboard container padding
- `--dashboard-gap` - Space between widgets
- `--widget-padding` - Widget internal padding
- `--kpi-spacing` - Space within KPI cards

**Typography Tokens:**
- `--kpi-value-font-size` - Large KPI number size
- `--kpi-value-font-weight` - KPI number weight
- `--kpi-label-font-size` - KPI label size
- `--widget-title-font-size` - Widget title size
- `--widget-title-font-weight` - Widget title weight

**Border & Radius:**
- `--widget-border-radius` - Widget corner radius
- `--widget-border-width` - Widget border thickness

**Shadow Tokens:**
- `--widget-shadow` - Widget elevation shadow
- `--dashboard-shadow` - Overall dashboard shadow

### Component-Specific Tokens

```css
/* Dashboard Container */
--dashboard-bg: var(--color-bg-secondary);
--dashboard-padding: var(--spacing-lg);
--dashboard-gap: var(--spacing-md);

/* Widget Cards */
--widget-bg: var(--color-white);
--widget-border-color: var(--color-border);
--widget-border-radius: var(--radius-lg);
--widget-shadow: var(--shadow-md);
--widget-padding: var(--spacing-lg);

/* KPI Cards */
--kpi-value-color: var(--color-text-primary);
--kpi-value-font-size: var(--font-size-4xl);
--kpi-value-font-weight: var(--font-weight-bold);
--kpi-label-color: var(--color-text-secondary);
--kpi-label-font-size: var(--font-size-sm);
--kpi-trend-positive: var(--color-success);
--kpi-trend-negative: var(--color-error);
--kpi-trend-neutral: var(--color-text-tertiary);
--kpi-sparkline-color: var(--color-primary);

/* Grid Layout */
--grid-columns: 12;
--grid-gap: var(--spacing-md);
--grid-row-height: 80px;
```

### Theme Support

- ✅ **Light Mode** - Clean, professional dashboards
- ✅ **Dark Mode** - Reduced eye strain for monitoring
- ✅ **High Contrast** - Clear data visibility
- ✅ **Custom Brand Themes** - Match company branding

### Example: Custom Dashboard Theming

```css
/* Executive dashboard theme */
:root[data-theme="executive-dashboard"] {
  /* Sophisticated color scheme */
  --dashboard-bg: #F8FAFC;
  --widget-bg: var(--color-white);
  --widget-shadow: var(--shadow-xl);

  /* Generous spacing */
  --dashboard-padding: var(--spacing-2xl);
  --widget-padding: var(--spacing-xl);

  /* Bold KPIs */
  --kpi-value-font-size: 3rem;
  --kpi-value-font-weight: var(--font-weight-extrabold);

  /* Elevated cards */
  --widget-border-radius: var(--radius-xl);
}
```

### Dark Mode Considerations

```css
:root[data-theme="dark"] {
  --dashboard-bg: var(--color-gray-950);
  --widget-bg: var(--color-gray-900);
  --widget-border-color: var(--color-gray-800);
  --kpi-value-color: var(--color-gray-50);
  --kpi-label-color: var(--color-gray-400);

  /* Softer shadows */
  --widget-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
}
```

### Accessibility via Tokens

- **High Contrast Mode**: Strong KPI number visibility
- **Color Independence**: Trends indicated by icons + color
- **Focus Indicators**: Clear focus states for interactive widgets
- **Reduced Motion**: Optional animation disabling

---

## Skill Structure

```yaml
---
name: dashboard-components
description: Comprehensive component library for dashboard and analytics interfaces. Use when building business intelligence dashboards, analytics tools, KPI displays, real-time monitoring systems, or data-heavy interfaces. Combines data visualization, tables, filters, and layout systems. Covers KPI cards, widget containers, grid layouts, real-time updates (WebSocket, polling, SSE), filter coordination, performance optimization, and responsive design. Triggered by requests to: build dashboard, create analytics interface, display KPIs, design monitoring system, or implement real-time data displays.
---
```

```
dashboards/
├── SKILL.md
├── references/
│   ├── kpi-cards.md
│   ├── layout-patterns.md
│   ├── real-time-updates.md
│   ├── filter-coordination.md
│   ├── performance-optimization.md
│   └── responsive-dashboards.md
├── examples/
│   ├── sales-dashboard.tsx
│   ├── analytics-dashboard.tsx
│   ├── monitoring-dashboard.tsx
│   └── customizable-dashboard.tsx
└── assets/
    ├── dashboard-templates/
    └── widget-library/
```

---

**END OF MASTER PLAN**
