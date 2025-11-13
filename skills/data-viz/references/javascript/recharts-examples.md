# Recharts Examples (JavaScript/TypeScript)

Working examples for common chart types using Recharts library.

## Installation

```bash
npm install recharts
```

## Bar Chart

```tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { category: 'Product A', revenue: 4000, expenses: 2400 },
  { category: 'Product B', revenue: 3000, expenses: 1398 },
  { category: 'Product C', revenue: 2000, expenses: 9800 },
  { category: 'Product D', revenue: 2780, expenses: 3908 },
];

export function RevenueBarChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="revenue" fill="#3B82F6" />
        <Bar dataKey="expenses" fill="#EF4444" />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

## Line Chart (Multi-Series)

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', actual: 4000, forecast: 3800 },
  { month: 'Feb', actual: 3000, forecast: 3200 },
  { month: 'Mar', actual: 5000, forecast: 4500 },
  { month: 'Apr', actual: 4500, forecast: 4800 },
];

export function SalesTrendChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="actual" stroke="#3B82F6" strokeWidth={2} />
        <Line type="monotone" dataKey="forecast" stroke="#10B981" strokeWidth={2} strokeDasharray="5 5" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## Pie Chart

```tsx
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Desktop', value: 400 },
  { name: 'Mobile', value: 300 },
  { name: 'Tablet', value: 200 },
];

const COLORS = ['#3B82F6', '#10B981', '#F59E0B'];

export function DeviceDistribution() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={80}
          label
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

## Area Chart (Stacked)

```tsx
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', productA: 2400, productB: 1398, productC: 2100 },
  { month: 'Feb', productA: 1398, productB: 2210, productC: 1800 },
  { month: 'Mar', productA: 9800, productB: 2290, productC: 2500 },
];

export function StackedRevenueChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Area type="monotone" dataKey="productA" stackId="1" stroke="#3B82F6" fill="#3B82F6" />
        <Area type="monotone" dataKey="productB" stackId="1" stroke="#10B981" fill="#10B981" />
        <Area type="monotone" dataKey="productC" stackId="1" stroke="#F59E0B" fill="#F59E0B" />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

## Scatter Plot

```tsx
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { x: 100, y: 200, name: 'A' },
  { x: 120, y: 100, name: 'B' },
  { x: 170, y: 300, name: 'C' },
  { x: 140, y: 250, name: 'D' },
  { x: 150, y: 400, name: 'E' },
];

export function CorrelationChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="x" name="Marketing Spend" unit="$K" />
        <YAxis dataKey="y" name="Revenue" unit="$K" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter name="Products" data={data} fill="#3B82F6" />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
```

## Composed Chart (Mixed Types)

```tsx
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', revenue: 590, profit: 120 },
  { month: 'Feb', revenue: 868, profit: 210 },
  { month: 'Mar', revenue: 1397, profit: 350 },
  { month: 'Apr', revenue: 1480, profit: 420 },
];

export function RevenueAndProfitChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="revenue" fill="#3B82F6" />
        <Line type="monotone" dataKey="profit" stroke="#10B981" strokeWidth={2} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
```

## Accessibility-Enhanced Chart

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useState } from 'react';

const data = [
  { month: 'Jan', sales: 4000 },
  { month: 'Feb', sales: 3000 },
  { month: 'Mar', sales: 5000 },
  { month: 'Apr', sales: 4500 },
];

export function AccessibleSalesChart() {
  const [viewMode, setViewMode] = useState('chart');

  return (
    <div>
      <div role="tablist" style={{ marginBottom: '16px' }}>
        <button
          role="tab"
          aria-selected={viewMode === 'chart'}
          onClick={() => setViewMode('chart')}
          style={{
            padding: '8px 16px',
            backgroundColor: viewMode === 'chart' ? '#3B82F6' : '#E5E7EB',
            color: viewMode === 'chart' ? 'white' : 'black',
            border: 'none',
            cursor: 'pointer',
          }}
        >
          Chart View
        </button>
        <button
          role="tab"
          aria-selected={viewMode === 'table'}
          onClick={() => setViewMode('table')}
          style={{
            padding: '8px 16px',
            backgroundColor: viewMode === 'table' ? '#3B82F6' : '#E5E7EB',
            color: viewMode === 'table' ? 'white' : 'black',
            border: 'none',
            cursor: 'pointer',
            marginLeft: '4px',
          }}
        >
          Table View
        </button>
      </div>

      {viewMode === 'chart' ? (
        <figure role="img" aria-label="Monthly sales trends showing growth from $3K in February to $5K in March">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="sales" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </figure>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <caption style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '8px' }}>
            Monthly Sales Data
          </caption>
          <thead>
            <tr style={{ backgroundColor: '#F3F4F6' }}>
              <th scope="col" style={{ padding: '12px', textAlign: 'left', border: '1px solid #D1D5DB' }}>
                Month
              </th>
              <th scope="col" style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                Sales ($)
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <th scope="row" style={{ padding: '12px', textAlign: 'left', border: '1px solid #D1D5DB' }}>
                  {row.month}
                </th>
                <td style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                  {row.sales.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
```

**All Recharts chart types:** Explore Recharts documentation at https://recharts.org/

For D3.js patterns, see `d3-patterns.md`.
For Plotly examples, see `plotly-examples.md`.
