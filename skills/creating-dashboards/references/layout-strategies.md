# Dashboard Layout Strategies

## Table of Contents
- [Grid System Fundamentals](#grid-system-fundamentals)
- [Fixed Layout Pattern](#fixed-layout-pattern)
- [Customizable Grid Layout](#customizable-grid-layout)
- [Template-Based Layouts](#template-based-layouts)
- [Responsive Breakpoints](#responsive-breakpoints)
- [Layout Persistence](#layout-persistence)
- [Performance Considerations](#performance-considerations)

## Grid System Fundamentals

### 12-Column Grid System
```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--dashboard-gap, 1rem);
  padding: var(--dashboard-padding, 1.5rem);
}

/* Widget spanning */
.widget-sm { grid-column: span 3; }  /* 1/4 width */
.widget-md { grid-column: span 4; }  /* 1/3 width */
.widget-lg { grid-column: span 6; }  /* 1/2 width */
.widget-xl { grid-column: span 8; }  /* 2/3 width */
.widget-full { grid-column: span 12; } /* Full width */
```

### CSS Grid Dashboard Layout
```tsx
function GridDashboard({ widgets }) {
  return (
    <div className="dashboard-grid">
      {widgets.map(widget => (
        <div
          key={widget.id}
          className={`widget-${widget.size}`}
          style={{
            gridRow: `span ${widget.height || 1}`,
          }}
        >
          <Widget {...widget} />
        </div>
      ))}
    </div>
  );
}
```

## Fixed Layout Pattern

### Executive Dashboard Layout
```tsx
const executiveLayout = {
  desktop: [
    { id: 'revenue', col: 0, row: 0, w: 3, h: 2 },
    { id: 'users', col: 3, row: 0, w: 3, h: 2 },
    { id: 'conversion', col: 6, row: 0, w: 3, h: 2 },
    { id: 'churn', col: 9, row: 0, w: 3, h: 2 },
    { id: 'chart', col: 0, row: 2, w: 8, h: 4 },
    { id: 'table', col: 8, row: 2, w: 4, h: 4 },
    { id: 'map', col: 0, row: 6, w: 6, h: 3 },
    { id: 'timeline', col: 6, row: 6, w: 6, h: 3 }
  ]
};

function FixedDashboard() {
  return (
    <div className="fixed-dashboard">
      {executiveLayout.desktop.map(item => (
        <div
          key={item.id}
          className="widget-container"
          style={{
            gridColumn: `${item.col + 1} / span ${item.w}`,
            gridRow: `${item.row + 1} / span ${item.h}`
          }}
        >
          <Widget id={item.id} />
        </div>
      ))}
    </div>
  );
}
```

### Predefined Layout Templates
```typescript
const layoutTemplates = {
  salesDashboard: {
    name: 'Sales Analytics',
    widgets: [
      { type: 'kpi', position: { x: 0, y: 0, w: 3, h: 2 } },
      { type: 'kpi', position: { x: 3, y: 0, w: 3, h: 2 } },
      { type: 'revenue-chart', position: { x: 0, y: 2, w: 6, h: 4 } },
      { type: 'product-table', position: { x: 6, y: 2, w: 6, h: 4 } }
    ]
  },

  operationsDashboard: {
    name: 'Operations Monitoring',
    widgets: [
      { type: 'status-grid', position: { x: 0, y: 0, w: 12, h: 2 } },
      { type: 'timeline', position: { x: 0, y: 2, w: 8, h: 3 } },
      { type: 'alerts', position: { x: 8, y: 2, w: 4, h: 3 } }
    ]
  }
};
```

## Customizable Grid Layout

### React Grid Layout Implementation
```tsx
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

function CustomizableDashboard() {
  const [layout, setLayout] = useState([
    { i: 'a', x: 0, y: 0, w: 4, h: 2 },
    { i: 'b', x: 4, y: 0, w: 4, h: 2 },
    { i: 'c', x: 8, y: 0, w: 4, h: 2 },
    { i: 'd', x: 0, y: 2, w: 6, h: 4 },
    { i: 'e', x: 6, y: 2, w: 6, h: 4 }
  ]);

  const onLayoutChange = (newLayout) => {
    setLayout(newLayout);
    // Save to localStorage or API
    localStorage.setItem('dashboardLayout', JSON.stringify(newLayout));
  };

  return (
    <GridLayout
      className="layout"
      layout={layout}
      cols={12}
      rowHeight={60}
      width={1200}
      onLayoutChange={onLayoutChange}
      draggableHandle=".widget-header"
      resizeHandles={['se']}
      compactType="vertical"
      preventCollision={false}
    >
      <div key="a"><KPIWidget title="Revenue" /></div>
      <div key="b"><KPIWidget title="Users" /></div>
      <div key="c"><KPIWidget title="Orders" /></div>
      <div key="d"><ChartWidget /></div>
      <div key="e"><TableWidget /></div>
    </GridLayout>
  );
}
```

### Responsive Grid Layout
```tsx
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

function ResponsiveDashboard() {
  const [layouts, setLayouts] = useState({
    lg: [
      { i: 'kpi1', x: 0, y: 0, w: 3, h: 2 },
      { i: 'kpi2', x: 3, y: 0, w: 3, h: 2 },
      { i: 'kpi3', x: 6, y: 0, w: 3, h: 2 },
      { i: 'kpi4', x: 9, y: 0, w: 3, h: 2 }
    ],
    md: [
      { i: 'kpi1', x: 0, y: 0, w: 5, h: 2 },
      { i: 'kpi2', x: 5, y: 0, w: 5, h: 2 },
      { i: 'kpi3', x: 0, y: 2, w: 5, h: 2 },
      { i: 'kpi4', x: 5, y: 2, w: 5, h: 2 }
    ],
    sm: [
      { i: 'kpi1', x: 0, y: 0, w: 6, h: 2 },
      { i: 'kpi2', x: 0, y: 2, w: 6, h: 2 },
      { i: 'kpi3', x: 0, y: 4, w: 6, h: 2 },
      { i: 'kpi4', x: 0, y: 6, w: 6, h: 2 }
    ]
  });

  return (
    <ResponsiveGridLayout
      layouts={layouts}
      breakpoints={{ lg: 1200, md: 996, sm: 768 }}
      cols={{ lg: 12, md: 10, sm: 6 }}
      rowHeight={60}
      onLayoutChange={(layout, layouts) => setLayouts(layouts)}
    >
      {/* Widgets */}
    </ResponsiveGridLayout>
  );
}
```

## Template-Based Layouts

### Dashboard Template System
```tsx
interface DashboardTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  widgets: WidgetConfig[];
  layout: LayoutConfig;
  filters: FilterConfig[];
}

const templates: DashboardTemplate[] = [
  {
    id: 'sales-overview',
    name: 'Sales Overview',
    description: 'Track sales performance and revenue metrics',
    category: 'Sales',
    widgets: [
      {
        type: 'kpi',
        dataSource: 'revenue',
        config: { period: 'monthly' }
      },
      {
        type: 'area-chart',
        dataSource: 'revenue-trend',
        config: { timeRange: '12months' }
      }
    ],
    layout: {
      desktop: { cols: 12, rowHeight: 80 },
      tablet: { cols: 8, rowHeight: 70 },
      mobile: { cols: 4, rowHeight: 60 }
    },
    filters: [
      { type: 'date-range', default: 'last-30-days' },
      { type: 'region', options: ['all', 'north', 'south'] }
    ]
  }
];

function TemplateSelector({ onSelect }) {
  return (
    <div className="template-grid">
      {templates.map(template => (
        <div
          key={template.id}
          className="template-card"
          onClick={() => onSelect(template)}
        >
          <h3>{template.name}</h3>
          <p>{template.description}</p>
          <span className="category">{template.category}</span>
        </div>
      ))}
    </div>
  );
}
```

### Applying Templates
```tsx
function DashboardFromTemplate({ templateId }) {
  const template = templates.find(t => t.id === templateId);
  const [widgets, setWidgets] = useState([]);

  useEffect(() => {
    // Initialize widgets from template
    const initializedWidgets = template.widgets.map((config, index) => ({
      id: `widget-${index}`,
      ...config,
      data: null,
      loading: true
    }));

    setWidgets(initializedWidgets);

    // Load data for each widget
    initializedWidgets.forEach(widget => {
      loadWidgetData(widget).then(data => {
        setWidgets(prev => prev.map(w =>
          w.id === widget.id ? { ...w, data, loading: false } : w
        ));
      });
    });
  }, [template]);

  return (
    <DashboardLayout
      layout={template.layout}
      widgets={widgets}
      filters={template.filters}
    />
  );
}
```

## Responsive Breakpoints

### Breakpoint Strategy
```typescript
const breakpoints = {
  mobile: 0,     // 0-767px
  tablet: 768,   // 768-1199px
  desktop: 1200, // 1200-1919px
  wide: 1920     // 1920px+
};

const getLayoutForBreakpoint = (width: number): LayoutType => {
  if (width >= breakpoints.wide) return 'wide';
  if (width >= breakpoints.desktop) return 'desktop';
  if (width >= breakpoints.tablet) return 'tablet';
  return 'mobile';
};
```

### Responsive Widget Sizing
```tsx
function ResponsiveWidget({ widget }) {
  const [dimensions, setDimensions] = useState({
    width: 'auto',
    height: 'auto'
  });

  useEffect(() => {
    const updateDimensions = () => {
      const viewport = window.innerWidth;

      if (viewport < 768) {
        // Mobile: full width, fixed height
        setDimensions({ width: '100%', height: '200px' });
      } else if (viewport < 1200) {
        // Tablet: half width, medium height
        setDimensions({ width: '50%', height: '250px' });
      } else {
        // Desktop: flexible based on widget type
        setDimensions({
          width: widget.defaultWidth || '25%',
          height: widget.defaultHeight || '300px'
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, [widget]);

  return (
    <div className="widget" style={dimensions}>
      <WidgetContent {...widget} />
    </div>
  );
}
```

### Mobile-First Layout
```css
/* Mobile First Approach */
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}

.widget {
  width: 100%;
  min-height: 200px;
}

/* Tablet */
@media (min-width: 768px) {
  .dashboard {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    padding: 1.5rem;
  }
}

/* Desktop */
@media (min-width: 1200px) {
  .dashboard {
    grid-template-columns: repeat(12, 1fr);
    gap: 2rem;
    padding: 2rem;
  }

  .widget-small { grid-column: span 3; }
  .widget-medium { grid-column: span 4; }
  .widget-large { grid-column: span 6; }
  .widget-full { grid-column: span 12; }
}
```

## Layout Persistence

### Saving User Layouts
```tsx
class LayoutPersistence {
  private storageKey = 'dashboard-layout';

  saveLayout(userId: string, layout: Layout) {
    const key = `${this.storageKey}-${userId}`;

    // Save to localStorage
    localStorage.setItem(key, JSON.stringify(layout));

    // Also save to backend
    fetch('/api/dashboard/layout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, layout })
    });
  }

  loadLayout(userId: string): Layout | null {
    const key = `${this.storageKey}-${userId}`;

    // Try localStorage first
    const stored = localStorage.getItem(key);
    if (stored) {
      return JSON.parse(stored);
    }

    // Fallback to backend
    return this.fetchLayoutFromBackend(userId);
  }

  async fetchLayoutFromBackend(userId: string): Promise<Layout | null> {
    try {
      const response = await fetch(`/api/dashboard/layout/${userId}`);
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to load layout:', error);
    }
    return null;
  }

  resetLayout(userId: string) {
    const key = `${this.storageKey}-${userId}`;
    localStorage.removeItem(key);

    fetch(`/api/dashboard/layout/${userId}`, {
      method: 'DELETE'
    });
  }
}
```

### Layout Versioning
```typescript
interface VersionedLayout {
  version: number;
  created: Date;
  modified: Date;
  layout: Layout;
  metadata: {
    browser: string;
    screenResolution: string;
    userId: string;
  };
}

function migrateLayout(layout: VersionedLayout): VersionedLayout {
  let migrated = { ...layout };

  // Migrate from v1 to v2
  if (layout.version === 1) {
    migrated.layout = convertV1ToV2(layout.layout);
    migrated.version = 2;
  }

  // Migrate from v2 to v3
  if (migrated.version === 2) {
    migrated.layout = convertV2ToV3(migrated.layout);
    migrated.version = 3;
  }

  return migrated;
}
```

## Performance Considerations

### Virtualized Grid for Large Dashboards
```tsx
import { FixedSizeGrid } from 'react-window';

function VirtualizedDashboard({ widgets, columns = 4 }) {
  const rowCount = Math.ceil(widgets.length / columns);

  const Cell = ({ columnIndex, rowIndex, style }) => {
    const index = rowIndex * columns + columnIndex;
    if (index >= widgets.length) return null;

    return (
      <div style={style}>
        <Widget {...widgets[index]} />
      </div>
    );
  };

  return (
    <FixedSizeGrid
      columnCount={columns}
      columnWidth={300}
      height={800}
      rowCount={rowCount}
      rowHeight={250}
      width={1200}
    >
      {Cell}
    </FixedSizeGrid>
  );
}
```

### Layout Optimization Techniques
```tsx
// Memoize expensive layout calculations
const calculateOptimalLayout = useMemo(() => {
  return (widgets: Widget[], containerWidth: number) => {
    // Complex layout algorithm
    const columns = Math.floor(containerWidth / 300);
    const layout = [];

    widgets.forEach((widget, index) => {
      const row = Math.floor(index / columns);
      const col = index % columns;

      layout.push({
        id: widget.id,
        x: col * (containerWidth / columns),
        y: row * 250,
        width: containerWidth / columns - 20,
        height: 230
      });
    });

    return layout;
  };
}, []);

// Debounce resize events
const useDebounceResize = (callback: Function, delay = 300) => {
  useEffect(() => {
    let timeoutId: NodeJS.Timeout;

    const handleResize = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(callback, delay);
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(timeoutId);
    };
  }, [callback, delay]);
};
```

### Progressive Layout Loading
```tsx
function ProgressiveDashboard({ widgets }) {
  const [visibleWidgets, setVisibleWidgets] = useState([]);
  const [loadingPhase, setLoadingPhase] = useState(0);

  useEffect(() => {
    // Phase 1: Load above-the-fold widgets
    const aboveFold = widgets.slice(0, 4);
    setVisibleWidgets(aboveFold);
    setLoadingPhase(1);

    // Phase 2: Load next batch after delay
    setTimeout(() => {
      const nextBatch = widgets.slice(4, 8);
      setVisibleWidgets(prev => [...prev, ...nextBatch]);
      setLoadingPhase(2);
    }, 100);

    // Phase 3: Load remaining widgets
    setTimeout(() => {
      const remaining = widgets.slice(8);
      setVisibleWidgets(prev => [...prev, ...remaining]);
      setLoadingPhase(3);
    }, 300);
  }, [widgets]);

  return (
    <div className="progressive-dashboard">
      {visibleWidgets.map(widget => (
        <Widget key={widget.id} {...widget} />
      ))}
      {loadingPhase < 3 && (
        <div className="loading-indicator">
          Loading more widgets...
        </div>
      )}
    </div>
  );
}
```