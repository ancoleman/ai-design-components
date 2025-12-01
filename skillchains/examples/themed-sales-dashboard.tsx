/**
 * Themed Sales Dashboard
 *
 * Demonstrates 3-skill chain: design-tokens + data-viz + forms
 *
 * Skills used:
 * - design-tokens: All styling (colors, spacing, typography)
 * - data-viz: Bar chart visualization
 * - forms: Date range filter inputs
 *
 * Features:
 * - Automatic theme switching (light/dark/brand)
 * - RTL support via CSS logical properties
 * - WCAG 2.1 AA accessible
 * - Interactive filtering
 */

import { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface SalesData {
  month: string;
  revenue: number;
  expenses: number;
  profit: number;
}

const mockData: SalesData[] = [
  { month: 'Jan', revenue: 45000, expenses: 28000, profit: 17000 },
  { month: 'Feb', revenue: 52000, expenses: 31000, profit: 21000 },
  { month: 'Mar', revenue: 48000, expenses: 29000, profit: 19000 },
  { month: 'Apr', revenue: 61000, expenses: 35000, profit: 26000 },
  { month: 'May', revenue: 58000, expenses: 33000, profit: 25000 },
  { month: 'Jun', revenue: 67000, expenses: 38000, profit: 29000 },
];

export function ThemedSalesDashboard() {
  const [startMonth, setStartMonth] = useState(0);
  const [endMonth, setEndMonth] = useState(5);

  // Filter data based on month range
  const filteredData = useMemo(() => {
    return mockData.slice(startMonth, endMonth + 1);
  }, [startMonth, endMonth]);

  return (
    <div style={{
      // design-tokens: spacing, colors
      padding: 'var(--spacing-xl)',
      backgroundColor: 'var(--color-bg-primary)',
      minHeight: '100vh'
    }}>
      {/* Header */}
      <header style={{
        marginBlockEnd: 'var(--spacing-xl)'
      }}>
        <h1 style={{
          // design-tokens: typography, colors
          fontSize: 'var(--font-size-4xl)',
          fontWeight: 'var(--font-weight-bold)',
          color: 'var(--color-text-primary)',
          marginBlockEnd: 'var(--spacing-sm)'
        }}>
          Sales Dashboard
        </h1>
        <p style={{
          fontSize: 'var(--font-size-base)',
          color: 'var(--color-text-secondary)'
        }}>
          Interactive analytics with theme support
        </p>
      </header>

      {/* Filter Controls (forms skill + design-tokens) */}
      <div style={{
        display: 'flex',
        gap: 'var(--spacing-md)',
        alignItems: 'flex-end',
        marginBlockEnd: 'var(--spacing-xl)',
        padding: 'var(--spacing-md)',
        backgroundColor: 'var(--color-bg-secondary)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <div style={{ flex: 1 }}>
          <label style={{
            display: 'block',
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'var(--font-weight-medium)',
            color: 'var(--color-text-secondary)',
            marginBlockEnd: 'var(--spacing-xs)'
          }}>
            Start Month
          </label>
          <select
            value={startMonth}
            onChange={(e) => setStartMonth(Number(e.target.value))}
            style={{
              width: '100%',
              height: 'var(--input-height)',
              paddingInline: 'var(--input-padding-inline)',
              backgroundColor: 'var(--input-bg)',
              border: '1px solid var(--input-border-color)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-size-base)',
              color: 'var(--input-text-color)',
              cursor: 'pointer'
            }}
          >
            {mockData.map((item, idx) => (
              <option key={idx} value={idx}>{item.month}</option>
            ))}
          </select>
        </div>

        <div style={{ flex: 1 }}>
          <label style={{
            display: 'block',
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'var(--font-weight-medium)',
            color: 'var(--color-text-secondary)',
            marginBlockEnd: 'var(--spacing-xs)'
          }}>
            End Month
          </label>
          <select
            value={endMonth}
            onChange={(e) => setEndMonth(Number(e.target.value))}
            style={{
              width: '100%',
              height: 'var(--input-height)',
              paddingInline: 'var(--input-padding-inline)',
              backgroundColor: 'var(--input-bg)',
              border: '1px solid var(--input-border-color)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-size-base)',
              color: 'var(--input-text-color)',
              cursor: 'pointer'
            }}
          >
            {mockData.map((item, idx) => (
              <option key={idx} value={idx}>{item.month}</option>
            ))}
          </select>
        </div>

        <div style={{
          fontSize: 'var(--font-size-sm)',
          color: 'var(--color-text-secondary)',
          paddingInline: 'var(--spacing-md)'
        }}>
          Showing {endMonth - startMonth + 1} months
        </div>
      </div>

      {/* Chart Card (data-viz skill + design-tokens) */}
      <div style={{
        padding: 'var(--spacing-lg)',
        backgroundColor: 'var(--color-bg-primary)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--color-border)',
        boxShadow: 'var(--shadow-md)'
      }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          fontWeight: 'var(--font-weight-semibold)',
          color: 'var(--color-text-primary)',
          marginBlockEnd: 'var(--spacing-lg)'
        }}>
          Revenue vs Expenses
        </h2>

        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={filteredData}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="var(--chart-grid-color)"
            />
            <XAxis
              dataKey="month"
              stroke="var(--chart-axis-color)"
              style={{
                fontSize: 'var(--font-size-sm)',
                fontFamily: 'var(--chart-font-family)'
              }}
            />
            <YAxis
              stroke="var(--chart-axis-color)"
              style={{
                fontSize: 'var(--font-size-sm)',
                fontFamily: 'var(--chart-font-family)'
              }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--chart-tooltip-bg)',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-sm)',
                boxShadow: 'var(--shadow-md)'
              }}
            />
            <Bar
              dataKey="revenue"
              fill="var(--chart-color-1)"
              name="Revenue"
            />
            <Bar
              dataKey="expenses"
              fill="var(--chart-color-2)"
              name="Expenses"
            />
          </BarChart>
        </ResponsiveContainer>

        {/* Summary Stats */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: 'var(--spacing-md)',
          marginBlockStart: 'var(--spacing-lg)'
        }}>
          {['revenue', 'expenses', 'profit'].map((metric) => {
            const total = filteredData.reduce((sum, item) => sum + item[metric as keyof SalesData], 0);
            return (
              <div
                key={metric}
                style={{
                  padding: 'var(--spacing-md)',
                  backgroundColor: 'var(--color-bg-secondary)',
                  borderRadius: 'var(--radius-md)',
                  textAlign: 'center'
                }}
              >
                <div style={{
                  fontSize: 'var(--font-size-sm)',
                  color: 'var(--color-text-secondary)',
                  textTransform: 'capitalize',
                  marginBlockEnd: 'var(--spacing-xs)'
                }}>
                  {metric}
                </div>
                <div style={{
                  fontSize: 'var(--font-size-3xl)',
                  fontWeight: 'var(--font-weight-bold)',
                  color: 'var(--color-text-primary)'
                }}>
                  ${(total / 1000).toFixed(1)}k
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Theme Info */}
      <div style={{
        marginBlockStart: 'var(--spacing-xl)',
        padding: 'var(--spacing-md)',
        backgroundColor: 'var(--color-info-bg)',
        border: '1px solid var(--color-info-border)',
        borderRadius: 'var(--radius-md)',
        fontSize: 'var(--font-size-sm)',
        color: 'var(--color-text-secondary)'
      }}>
        <strong>💡 Theme Support:</strong> This dashboard uses design-tokens for ALL styling.
        Try switching themes to see automatic updates!
      </div>
    </div>
  );
}

/**
 * Usage:
 *
 * import { ThemeProvider } from '../skills/design-tokens/examples/ThemeProvider';
 * import { ThemedSalesDashboard } from './themed-sales-dashboard';
 *
 * function App() {
 *   return (
 *     <ThemeProvider>
 *       <ThemedSalesDashboard />
 *     </ThemeProvider>
 *   );
 * }
 *
 * // Theme switching automatically updates:
 * // - Chart colors (data-viz tokens)
 * // - Input styling (forms tokens)
 * // - All spacing, typography, borders
 */
