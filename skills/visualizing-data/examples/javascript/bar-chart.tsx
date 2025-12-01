import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * Example: Sales Revenue Bar Chart
 *
 * Purpose: Compare revenue across product categories
 * Data: Categorical (product categories) + Continuous (revenue, expenses)
 * Chart Type: Grouped Bar Chart
 * Accessibility: Includes aria-label, high contrast colors
 */

const salesData = [
  { category: 'Electronics', revenue: 45000, expenses: 28000 },
  { category: 'Clothing', revenue: 38000, expenses: 22000 },
  { category: 'Home & Garden', revenue: 52000, expenses: 31000 },
  { category: 'Sports', revenue: 29000, expenses: 18000 },
  { category: 'Books', revenue: 21000, expenses: 12000 },
];

export function SalesRevenueChart() {
  return (
    <div
      role="img"
      aria-label="Sales revenue and expenses by category. Electronics generated $45K revenue with $28K expenses. Highest revenue was Home & Garden at $52K."
    >
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={salesData}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" />
          <YAxis
            label={{ value: 'Amount ($)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            formatter={(value) => `$${value.toLocaleString()}`}
          />
          <Legend />
          <Bar dataKey="revenue" fill="#3B82F6" name="Revenue" />
          <Bar dataKey="expenses" fill="#EF4444" name="Expenses" />
        </BarChart>
      </ResponsiveContainer>

      {/* Screen reader table alternative */}
      <table style={{ position: 'absolute', left: '-10000px', top: 'auto' }}>
        <caption>Sales Revenue and Expenses by Category</caption>
        <thead>
          <tr>
            <th scope="col">Category</th>
            <th scope="col">Revenue ($)</th>
            <th scope="col">Expenses ($)</th>
          </tr>
        </thead>
        <tbody>
          {salesData.map((row, i) => (
            <tr key={i}>
              <th scope="row">{row.category}</th>
              <td>{row.revenue.toLocaleString()}</td>
              <td>{row.expenses.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```
