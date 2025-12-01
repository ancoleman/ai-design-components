# Dashboard Libraries Implementation Guide

## Table of Contents
- [Tremor Quick Start](#tremor-quick-start)
- [React Grid Layout Setup](#react-grid-layout-setup)
- [Combining Libraries](#combining-libraries)
- [Migration Strategies](#migration-strategies)
- [Advanced Configurations](#advanced-configurations)
- [Troubleshooting](#troubleshooting)

## Tremor Quick Start

### Installation & Setup
```bash
# Install Tremor with Tailwind CSS
npm install @tremor/react tailwindcss @tailwindcss/forms

# Initialize Tailwind if not already configured
npx tailwindcss init -p
```

### Tailwind Configuration for Tremor
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@tremor/**/*.{js,ts,jsx,tsx}', // Tremor components
  ],
  theme: {
    extend: {
      colors: {
        tremor: {
          brand: {
            faint: '#eff6ff',
            muted: '#bfdbfe',
            subtle: '#60a5fa',
            DEFAULT: '#3b82f6',
            emphasis: '#1d4ed8',
            inverted: '#ffffff',
          },
          background: {
            muted: '#f9fafb',
            subtle: '#f3f4f6',
            DEFAULT: '#ffffff',
            emphasis: '#374151',
          },
          // Additional Tremor colors...
        }
      }
    }
  },
  plugins: [require('@tailwindcss/forms')]
};
```

### Basic Tremor Dashboard
```tsx
import {
  Card,
  Title,
  Text,
  Tab,
  TabList,
  TabGroup,
  TabPanel,
  TabPanels,
  Grid,
  Metric,
  BadgeDelta,
  Flex,
  ProgressBar,
  AreaChart,
  BarChart,
  DonutChart,
  Table,
  TableHead,
  TableRow,
  TableHeaderCell,
  TableBody,
  TableCell
} from '@tremor/react';

function TremorDashboard() {
  return (
    <main className="p-6 sm:p-10">
      <Title>Analytics Dashboard</Title>
      <Text>Track your key metrics and performance indicators</Text>

      {/* KPI Cards Row */}
      <Grid numItemsSm={2} numItemsLg={4} className="gap-6 mt-6">
        <Card>
          <Flex alignItems="start">
            <div>
              <Text>Revenue</Text>
              <Metric>$45,231.89</Metric>
            </div>
            <BadgeDelta deltaType="increase">12.5%</BadgeDelta>
          </Flex>
        </Card>

        <Card>
          <Flex alignItems="start">
            <div>
              <Text>New Customers</Text>
              <Metric>1,234</Metric>
            </div>
            <BadgeDelta deltaType="decrease">-2.3%</BadgeDelta>
          </Flex>
        </Card>

        <Card>
          <Flex alignItems="start">
            <div>
              <Text>Active Users</Text>
              <Metric>8,456</Metric>
            </div>
            <BadgeDelta deltaType="increase">5.1%</BadgeDelta>
          </Flex>
        </Card>

        <Card>
          <Flex alignItems="start">
            <div>
              <Text>Retention Rate</Text>
              <Metric>92.5%</Metric>
            </div>
            <BadgeDelta deltaType="unchanged">0.0%</BadgeDelta>
          </Flex>
        </Card>
      </Grid>

      {/* Charts Section */}
      <div className="mt-6">
        <Card>
          <Title>Revenue Trend</Title>
          <AreaChart
            className="h-72 mt-4"
            data={revenueData}
            index="date"
            categories={["Revenue", "Target"]}
            colors={["blue", "gray"]}
            valueFormatter={dataFormatter}
          />
        </Card>
      </div>

      {/* Table Section */}
      <Card className="mt-6">
        <Title>Recent Transactions</Title>
        <Table className="mt-5">
          <TableHead>
            <TableRow>
              <TableHeaderCell>Transaction</TableHeaderCell>
              <TableHeaderCell>Amount</TableHeaderCell>
              <TableHeaderCell>Status</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map(item => (
              <TableRow key={item.id}>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.amount}</TableCell>
                <TableCell>{item.status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </main>
  );
}
```

### Advanced Tremor Components

#### Multi-Metric Cards
```tsx
function MultiMetricCard() {
  return (
    <Card className="max-w-lg mx-auto">
      <Flex className="space-x-8" justifyContent="start" alignItems="baseline">
        <div>
          <Text>Sales</Text>
          <Metric>$12,699</Metric>
          <Text className="mt-2">from $10,456</Text>
        </div>
        <div>
          <Text>Profit</Text>
          <Metric>$4,034</Metric>
          <Text className="mt-2">from $3,210</Text>
        </div>
      </Flex>
      <ProgressBar value={32} className="mt-4" />
      <Text className="mt-2">32% of annual target</Text>
    </Card>
  );
}
```

#### Tabbed Dashboard
```tsx
function TabbedDashboard() {
  return (
    <Card>
      <TabGroup>
        <TabList className="mt-8">
          <Tab>Overview</Tab>
          <Tab>Detail</Tab>
          <Tab>Analysis</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Grid numItemsMd={2} numItemsLg={3} className="gap-6 mt-6">
              {/* Overview widgets */}
            </Grid>
          </TabPanel>
          <TabPanel>
            {/* Detailed charts */}
          </TabPanel>
          <TabPanel>
            {/* Analysis tables */}
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </Card>
  );
}
```

## React Grid Layout Setup

### Installation
```bash
npm install react-grid-layout

# Required CSS
npm install react-resizable
```

### Basic Setup
```tsx
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

function BasicGridDashboard() {
  const layout = [
    { i: 'a', x: 0, y: 0, w: 4, h: 2 },
    { i: 'b', x: 4, y: 0, w: 4, h: 2 },
    { i: 'c', x: 8, y: 0, w: 4, h: 2 },
    { i: 'd', x: 0, y: 2, w: 12, h: 4 }
  ];

  return (
    <GridLayout
      className="layout"
      layout={layout}
      cols={12}
      rowHeight={80}
      width={1200}
    >
      <div key="a" className="widget">
        <KPICard title="Revenue" value="$45K" />
      </div>
      <div key="b" className="widget">
        <KPICard title="Users" value="1.2K" />
      </div>
      <div key="c" className="widget">
        <KPICard title="Orders" value="342" />
      </div>
      <div key="d" className="widget">
        <ChartWidget />
      </div>
    </GridLayout>
  );
}
```

### Responsive Grid Layout
```tsx
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

function ResponsiveDashboard() {
  const [layouts, setLayouts] = useState(getFromLS('layouts') || {});

  const handleLayoutChange = (layout, layouts) => {
    saveToLS('layouts', layouts);
    setLayouts(layouts);
  };

  return (
    <ResponsiveGridLayout
      className="layout"
      layouts={layouts}
      breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
      cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
      rowHeight={60}
      onLayoutChange={handleLayoutChange}
    >
      <div key="1">Widget 1</div>
      <div key="2">Widget 2</div>
      <div key="3">Widget 3</div>
    </ResponsiveGridLayout>
  );
}

// Local Storage helpers
function getFromLS(key) {
  let ls = {};
  if (global.localStorage) {
    try {
      ls = JSON.parse(global.localStorage.getItem('rgl-8')) || {};
    } catch (e) {}
  }
  return ls[key];
}

function saveToLS(key, value) {
  if (global.localStorage) {
    global.localStorage.setItem(
      'rgl-8',
      JSON.stringify({
        [key]: value
      })
    );
  }
}
```

### Advanced Grid Features

#### Drag Handle & Resize Restrictions
```tsx
function RestrictedGridDashboard() {
  const layout = [
    {
      i: 'header',
      x: 0,
      y: 0,
      w: 12,
      h: 1,
      static: true // Cannot be moved or resized
    },
    {
      i: 'kpi1',
      x: 0,
      y: 1,
      w: 3,
      h: 2,
      minW: 2,
      maxW: 4,
      minH: 1,
      maxH: 3
    },
    {
      i: 'chart',
      x: 3,
      y: 1,
      w: 9,
      h: 4,
      minW: 6,
      minH: 3
    }
  ];

  return (
    <GridLayout
      layout={layout}
      cols={12}
      rowHeight={60}
      draggableHandle=".drag-handle" // Only draggable by handle
      resizeHandles={['se', 'sw']} // Only bottom corners
      compactType="vertical"
      preventCollision={false}
    >
      <div key="header" className="widget">
        <h1>Dashboard Header (Static)</h1>
      </div>
      <div key="kpi1" className="widget">
        <div className="drag-handle">⋮⋮</div>
        <KPIWidget />
      </div>
      <div key="chart" className="widget">
        <div className="drag-handle">⋮⋮</div>
        <ChartWidget />
      </div>
    </GridLayout>
  );
}
```

#### Widget Catalog with Add/Remove
```tsx
function CustomizableDashboard() {
  const [widgets, setWidgets] = useState([
    { id: 'widget-1', type: 'kpi', x: 0, y: 0, w: 3, h: 2 }
  ]);

  const widgetCatalog = [
    { type: 'kpi', name: 'KPI Card', defaultSize: { w: 3, h: 2 } },
    { type: 'chart', name: 'Chart', defaultSize: { w: 6, h: 4 } },
    { type: 'table', name: 'Table', defaultSize: { w: 6, h: 3 } }
  ];

  const addWidget = (type) => {
    const catalogItem = widgetCatalog.find(w => w.type === type);
    const newWidget = {
      id: `widget-${Date.now()}`,
      type,
      x: 0,
      y: Infinity, // Will be placed at bottom
      ...catalogItem.defaultSize
    };
    setWidgets([...widgets, newWidget]);
  };

  const removeWidget = (id) => {
    setWidgets(widgets.filter(w => w.id !== id));
  };

  return (
    <div>
      {/* Widget Catalog */}
      <div className="widget-catalog">
        {widgetCatalog.map(item => (
          <button
            key={item.type}
            onClick={() => addWidget(item.type)}
          >
            Add {item.name}
          </button>
        ))}
      </div>

      {/* Grid Dashboard */}
      <ResponsiveGridLayout>
        {widgets.map(widget => (
          <div key={widget.id} data-grid={widget}>
            <div className="widget-wrapper">
              <button
                className="remove-btn"
                onClick={() => removeWidget(widget.id)}
              >
                ×
              </button>
              {renderWidget(widget)}
            </div>
          </div>
        ))}
      </ResponsiveGridLayout>
    </div>
  );
}
```

## Combining Libraries

### Tremor Components in Grid Layout
```tsx
import { Card, Metric, Text, AreaChart } from '@tremor/react';
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

function HybridDashboard() {
  const layouts = {
    lg: [
      { i: 'revenue-kpi', x: 0, y: 0, w: 3, h: 2 },
      { i: 'users-kpi', x: 3, y: 0, w: 3, h: 2 },
      { i: 'chart', x: 0, y: 2, w: 6, h: 4 },
      { i: 'table', x: 6, y: 0, w: 6, h: 6 }
    ]
  };

  return (
    <ResponsiveGridLayout
      layouts={layouts}
      breakpoints={{ lg: 1200, md: 996, sm: 768 }}
      cols={{ lg: 12, md: 10, sm: 6 }}
      rowHeight={60}
    >
      {/* Tremor KPI Card */}
      <div key="revenue-kpi">
        <Card className="h-full">
          <Text>Revenue</Text>
          <Metric>$45,231</Metric>
        </Card>
      </div>

      {/* Tremor KPI Card */}
      <div key="users-kpi">
        <Card className="h-full">
          <Text>Active Users</Text>
          <Metric>1,234</Metric>
        </Card>
      </div>

      {/* Tremor Chart */}
      <div key="chart">
        <Card className="h-full">
          <AreaChart
            data={chartData}
            index="date"
            categories={["Sales"]}
            colors={["blue"]}
          />
        </Card>
      </div>

      {/* Custom Table Widget */}
      <div key="table">
        <Card className="h-full">
          <CustomTableWidget />
        </Card>
      </div>
    </ResponsiveGridLayout>
  );
}
```

### Custom Widget Wrapper
```tsx
function WidgetWrapper({ widget, children }) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  return (
    <Card className="h-full relative">
      {/* Widget Header */}
      <div className="widget-header drag-handle flex justify-between items-center mb-4">
        <Title>{widget.title}</Title>
        <div className="widget-actions">
          <button className="refresh-btn">↻</button>
          <button className="settings-btn">⚙</button>
        </div>
      </div>

      {/* Widget Content */}
      <div className="widget-content">
        {isLoading ? (
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        ) : hasError ? (
          <div className="error-state">
            <Text>Failed to load widget</Text>
            <button onClick={() => setHasError(false)}>Retry</button>
          </div>
        ) : (
          children
        )}
      </div>

      {/* Resize Handle (for react-grid-layout) */}
      <span className="react-resizable-handle react-resizable-handle-se" />
    </Card>
  );
}
```

## Migration Strategies

### Migrating from Static to Grid Layout
```tsx
// Before: Static Dashboard
function StaticDashboard() {
  return (
    <div className="dashboard">
      <div className="row">
        <KPICard />
        <KPICard />
        <KPICard />
      </div>
      <div className="row">
        <ChartWidget />
        <TableWidget />
      </div>
    </div>
  );
}

// After: Grid Layout Dashboard
function MigratedDashboard() {
  // Convert static positions to grid layout
  const staticToGridLayout = () => {
    return [
      { i: 'kpi-1', x: 0, y: 0, w: 4, h: 2 },
      { i: 'kpi-2', x: 4, y: 0, w: 4, h: 2 },
      { i: 'kpi-3', x: 8, y: 0, w: 4, h: 2 },
      { i: 'chart', x: 0, y: 2, w: 6, h: 4 },
      { i: 'table', x: 6, y: 2, w: 6, h: 4 }
    ];
  };

  const [layout, setLayout] = useState(staticToGridLayout());
  const [isCustomizable, setIsCustomizable] = useState(false);

  return (
    <>
      <button onClick={() => setIsCustomizable(!isCustomizable)}>
        {isCustomizable ? 'Lock Layout' : 'Customize Layout'}
      </button>

      <GridLayout
        layout={layout}
        cols={12}
        rowHeight={60}
        width={1200}
        isDraggable={isCustomizable}
        isResizable={isCustomizable}
        onLayoutChange={setLayout}
      >
        <div key="kpi-1"><KPICard /></div>
        <div key="kpi-2"><KPICard /></div>
        <div key="kpi-3"><KPICard /></div>
        <div key="chart"><ChartWidget /></div>
        <div key="table"><TableWidget /></div>
      </GridLayout>
    </>
  );
}
```

## Advanced Configurations

### Dynamic Grid Configuration
```tsx
function DynamicGridConfig() {
  const [config, setConfig] = useState({
    cols: 12,
    rowHeight: 60,
    compactType: 'vertical',
    margin: [10, 10]
  });

  const updateConfig = (key, value) => {
    setConfig({ ...config, [key]: value });
  };

  return (
    <div>
      {/* Configuration Panel */}
      <div className="config-panel">
        <label>
          Columns:
          <input
            type="number"
            value={config.cols}
            onChange={(e) => updateConfig('cols', parseInt(e.target.value))}
          />
        </label>
        <label>
          Row Height:
          <input
            type="number"
            value={config.rowHeight}
            onChange={(e) => updateConfig('rowHeight', parseInt(e.target.value))}
          />
        </label>
        <label>
          Compact Type:
          <select
            value={config.compactType}
            onChange={(e) => updateConfig('compactType', e.target.value)}
          >
            <option value="vertical">Vertical</option>
            <option value="horizontal">Horizontal</option>
            <option value={null}>None</option>
          </select>
        </label>
      </div>

      {/* Grid with dynamic config */}
      <GridLayout
        {...config}
        width={1200}
      >
        {/* Widgets */}
      </GridLayout>
    </div>
  );
}
```

### Theme Integration
```tsx
// Tremor with custom theme
const customTheme = {
  dark: {
    background: '#1a1a1a',
    card: '#2a2a2a',
    text: '#ffffff',
    border: '#3a3a3a'
  },
  light: {
    background: '#ffffff',
    card: '#f9fafb',
    text: '#111827',
    border: '#e5e7eb'
  }
};

function ThemedDashboard({ theme = 'light' }) {
  const colors = customTheme[theme];

  return (
    <div
      className="dashboard"
      style={{
        backgroundColor: colors.background,
        color: colors.text
      }}
    >
      <ResponsiveGridLayout>
        {widgets.map(widget => (
          <div key={widget.id}>
            <Card
              style={{
                backgroundColor: colors.card,
                borderColor: colors.border
              }}
            >
              {renderWidget(widget)}
            </Card>
          </div>
        ))}
      </ResponsiveGridLayout>
    </div>
  );
}
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Grid Layout CSS Not Loading
```tsx
// Ensure CSS imports are correct
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

// Or import in your main CSS file
/* styles.css */
@import '~react-grid-layout/css/styles.css';
@import '~react-resizable/css/styles.css';
```

#### 2. Widgets Overlapping
```tsx
// Set preventCollision to true
<GridLayout
  preventCollision={true}
  compactType="vertical"
  // This will prevent widgets from overlapping
>
```

#### 3. Responsive Layout Not Working
```tsx
// Must wrap with WidthProvider
const ResponsiveGridLayout = WidthProvider(Responsive);

// Don't pass width prop when using WidthProvider
<ResponsiveGridLayout
  // width={1200} // Don't do this
  layouts={layouts}
>
```

#### 4. Tremor Components Not Styled
```javascript
// Ensure Tailwind processes Tremor files
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './node_modules/@tremor/**/*.{js,ts,jsx,tsx}', // Important!
  ]
};
```

#### 5. Performance Issues with Many Widgets
```tsx
// Use React.memo for widget components
const MemoizedWidget = React.memo(({ data }) => {
  return <Card>{/* Widget content */}</Card>;
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.data === nextProps.data;
});

// Virtualize if > 50 widgets
import { FixedSizeGrid } from 'react-window';
```