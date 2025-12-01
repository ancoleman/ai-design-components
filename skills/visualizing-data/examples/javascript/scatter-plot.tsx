import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis } from 'recharts';

/**
 * Example: Marketing Spend vs Revenue Scatter Plot
 *
 * Purpose: Explore correlation between marketing spend and revenue
 * Data: Two continuous variables (spend, revenue)
 * Chart Type: Scatter Plot
 * Accessibility: aria-label, colorblind-safe, correlation description
 */

const correlationData = [
  { spend: 100, revenue: 200, product: 'Product A' },
  { spend: 120, revenue: 180, product: 'Product B' },
  { spend: 170, revenue: 320, product: 'Product C' },
  { spend: 140, revenue: 250, product: 'Product D' },
  { spend: 150, revenue: 380, product: 'Product E' },
  { spend: 180, revenue: 350, product: 'Product F' },
  { spend: 160, revenue: 400, product: 'Product G' },
  { spend: 190, revenue: 420, product: 'Product H' },
  { spend: 200, revenue: 450, product: 'Product I' },
  { spend: 210, revenue: 480, product: 'Product J' },
];

export function MarketingCorrelationChart() {
  return (
    <figure
      role="img"
      aria-label="Scatter plot showing positive correlation between marketing spend and revenue. As spending increases from $100K to $210K, revenue increases from $200K to $480K, indicating effective marketing ROI."
    >
      <figcaption style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>
        Marketing Spend vs Revenue Correlation
      </figcaption>

      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="spend"
            name="Marketing Spend"
            unit="K"
            label={{ value: 'Marketing Spend ($K)', position: 'insideBottom', offset: -10 }}
          />
          <YAxis
            type="number"
            dataKey="revenue"
            name="Revenue"
            unit="K"
            label={{ value: 'Revenue ($K)', angle: -90, position: 'insideLeft' }}
          />
          <ZAxis range={[100, 100]} />
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div
                    style={{
                      backgroundColor: 'white',
                      padding: '12px',
                      border: '1px solid #ccc',
                      borderRadius: '4px',
                    }}
                  >
                    <p style={{ margin: 0, fontWeight: 'bold' }}>{data.product}</p>
                    <p style={{ margin: '4px 0 0 0', fontSize: '14px' }}>
                      Spend: ${data.spend}K
                    </p>
                    <p style={{ margin: '4px 0 0 0', fontSize: '14px' }}>
                      Revenue: ${data.revenue}K
                    </p>
                    <p style={{ margin: '4px 0 0 0', fontSize: '14px', color: '#10B981' }}>
                      ROI: {((data.revenue / data.spend - 1) * 100).toFixed(1)}%
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Scatter
            name="Products"
            data={correlationData}
            fill="#3B82F6"
            fillOpacity={0.6}
            stroke="#1E40AF"
            strokeWidth={2}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </figure>
  );
}
```
