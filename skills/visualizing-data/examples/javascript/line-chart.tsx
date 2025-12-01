import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * Example: Monthly Sales Trend Line Chart
 *
 * Purpose: Show sales trends over time
 * Data: Temporal (months) + Continuous (sales values)
 * Chart Type: Line Chart
 * Accessibility: aria-label, colorblind-safe colors, data table
 */

const monthlyData = [
  { month: 'Jan', sales: 4000, target: 3500 },
  { month: 'Feb', sales: 3000, target: 3500 },
  { month: 'Mar', sales: 5000, target: 4000 },
  { month: 'Apr', sales: 4500, target: 4000 },
  { month: 'May', sales: 6000, target: 4500 },
  { month: 'Jun', sales: 5500, target: 4500 },
];

export function MonthlySalesTrend() {
  return (
    <figure
      role="img"
      aria-label="Monthly sales trends from January to June 2024. Sales fluctuated between $3K and $6K, with peak in May at $6K, consistently meeting or exceeding targets."
    >
      <figcaption style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>
        Monthly Sales Trend (Jan-Jun 2024)
      </figcaption>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={monthlyData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis
            label={{ value: 'Sales ($)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            formatter={(value) => `$${value.toLocaleString()}`}
          />
          <Legend />

          {/* Actual sales - solid blue line */}
          <Line
            type="monotone"
            dataKey="sales"
            stroke="#3B82F6"
            strokeWidth={3}
            dot={{ fill: '#3B82F6', strokeWidth: 2, r: 5 }}
            name="Actual Sales"
          />

          {/* Target - dashed green line */}
          <Line
            type="monotone"
            dataKey="target"
            stroke="#10B981"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#10B981', strokeWidth: 2, r: 4 }}
            name="Target"
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Alternative data table for accessibility */}
      <details style={{ marginTop: '16px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: '500' }}>
          View as Data Table
        </summary>
        <table style={{ width: '100%', marginTop: '8px', borderCollapse: 'collapse' }}>
          <caption className="sr-only">Monthly Sales Data</caption>
          <thead>
            <tr style={{ backgroundColor: '#F3F4F6' }}>
              <th scope="col" style={{ padding: '12px', textAlign: 'left', border: '1px solid #D1D5DB' }}>
                Month
              </th>
              <th scope="col" style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                Actual Sales
              </th>
              <th scope="col" style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                Target
              </th>
              <th scope="col" style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                Variance
              </th>
            </tr>
          </thead>
          <tbody>
            {monthlyData.map((row, i) => {
              const variance = row.sales - row.target;
              const percentVariance = ((variance / row.target) * 100).toFixed(1);

              return (
                <tr key={i}>
                  <th scope="row" style={{ padding: '12px', textAlign: 'left', border: '1px solid #D1D5DB' }}>
                    {row.month}
                  </th>
                  <td style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                    ${row.sales.toLocaleString()}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'right', border: '1px solid #D1D5DB' }}>
                    ${row.target.toLocaleString()}
                  </td>
                  <td
                    style={{
                      padding: '12px',
                      textAlign: 'right',
                      border: '1px solid #D1D5DB',
                      color: variance >= 0 ? '#10B981' : '#EF4444',
                    }}
                  >
                    {variance >= 0 ? '+' : ''}${variance.toLocaleString()} ({percentVariance}%)
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </details>
    </figure>
  );
}
```
