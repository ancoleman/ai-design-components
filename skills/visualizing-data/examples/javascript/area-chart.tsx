import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

/**
 * Example: Stacked Area Chart for Product Revenue
 *
 * Purpose: Show composition over time
 * Data: Temporal + Multiple continuous series
 * Chart Type: Stacked Area Chart
 * Use case: Revenue breakdown by product line over time
 */

const quarterlyData = [
  { quarter: 'Q1 2023', productA: 2400, productB: 1398, productC: 2100 },
  { quarter: 'Q2 2023', productA: 1398, productB: 2210, productC: 1800 },
  { quarter: 'Q3 2023', productA: 2800, productB: 2290, productC: 2500 },
  { quarter: 'Q4 2023', productA: 3908, productB: 2000, productC: 2800 },
  { quarter: 'Q1 2024', productA: 4800, productB: 2181, productC: 3200 },
  { quarter: 'Q2 2024', productA: 3800, productB: 2500, productC: 3500 },
];

// Colorblind-safe colors
const COLORS = {
  productA: '#648FFF', // Blue
  productB: '#785EF0', // Purple
  productC: '#FE6100', // Orange
};

export function QuarterlyRevenueAreaChart() {
  return (
    <figure
      role="img"
      aria-label="Quarterly revenue trends from Q1 2023 to Q2 2024 showing growth across all product lines. Total revenue increased from $5.9K to $9.8K."
    >
      <figcaption style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>
        Quarterly Revenue by Product Line
      </figcaption>

      <ResponsiveContainer width="100%" height={400}>
        <AreaChart
          data={quarterlyData}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="quarter" />
          <YAxis
            label={{ value: 'Revenue ($)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            formatter={(value) => `$${value.toLocaleString()}`}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #ccc',
              borderRadius: '4px',
              padding: '8px',
            }}
          />
          <Legend />

          <Area
            type="monotone"
            dataKey="productA"
            stackId="1"
            stroke={COLORS.productA}
            fill={COLORS.productA}
            fillOpacity={0.6}
            name="Product A"
          />
          <Area
            type="monotone"
            dataKey="productB"
            stackId="1"
            stroke={COLORS.productB}
            fill={COLORS.productB}
            fillOpacity={0.6}
            name="Product B"
          />
          <Area
            type="monotone"
            dataKey="productC"
            stackId="1"
            stroke={COLORS.productC}
            fill={COLORS.productC}
            fillOpacity={0.6}
            name="Product C"
          />
        </AreaChart>
      </ResponsiveContainer>
    </figure>
  );
}
```
