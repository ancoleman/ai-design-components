import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * Example: Device Distribution Pie Chart
 *
 * Purpose: Show composition/part-to-whole
 * Data: Categorical with percentages
 * Chart Type: Pie Chart
 * Note: Only use for 2-6 categories
 * Accessibility: Patterns + colors, data table
 */

const deviceData = [
  { name: 'Desktop', value: 400, percentage: 44.4 },
  { name: 'Mobile', value: 300, percentage: 33.3 },
  { name: 'Tablet', value: 200, percentage: 22.2 },
];

// Colorblind-safe colors
const COLORS = ['#648FFF', '#785EF0', '#DC267F'];

// SVG patterns for additional differentiation
const renderPatterns = () => (
  <defs>
    <pattern id="diagonal" width="4" height="4" patternUnits="userSpaceOnUse">
      <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" stroke="currentColor" strokeWidth="0.5" />
    </pattern>
    <pattern id="dots" width="4" height="4" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="currentColor" />
    </pattern>
    <pattern id="grid" width="4" height="4" patternUnits="userSpaceOnUse">
      <path d="M 4 0 L 0 0 0 4" fill="none" stroke="currentColor" strokeWidth="0.5" />
    </pattern>
  </defs>
);

export function DeviceDistributionChart() {
  return (
    <figure
      role="img"
      aria-label="Device distribution shows Desktop usage at 44%, Mobile at 33%, and Tablet at 22%"
    >
      <figcaption style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>
        Traffic by Device Type
      </figcaption>

      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={deviceData}
            cx="50%"
            cy="50%"
            labelLine={true}
            label={({ name, percentage }) => `${name}: ${percentage.toFixed(1)}%`}
            outerRadius={120}
            fill="#8884d8"
            dataKey="value"
          >
            {deviceData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name) => [
              `${value} users (${deviceData.find(d => d.name === name)?.percentage.toFixed(1)}%)`,
              name,
            ]}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>

      {/* Data table for accessibility */}
      <details style={{ marginTop: '16px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: '500' }}>
          View as Data Table
        </summary>
        <table style={{ width: '100%', marginTop: '8px', borderCollapse: 'collapse' }}>
          <caption className="sr-only">Device Distribution</caption>
          <thead>
            <tr style={{ backgroundColor: '#F3F4F6' }}>
              <th scope="col" style={{ padding: '12px', textAlign: 'left', border: '1px solid #D1D5DB' }}>
                Device Type
              </th>
              <th scope="col" style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                Users
              </th>
              <th scope="col" style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                Percentage
              </th>
            </tr>
          </thead>
          <tbody>
            {deviceData.map((row, i) => (
              <tr key={i}>
                <th scope="row" style={{ padding: '12px', textAlign: 'left', border: '1px solid #D1D5DB' }}>
                  {row.name}
                </th>
                <td style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                  {row.value}
                </td>
                <td style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                  {row.percentage.toFixed(1)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </figure>
  );
}
```
