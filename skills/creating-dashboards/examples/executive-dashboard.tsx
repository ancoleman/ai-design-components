import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Users, DollarSign, ShoppingCart, Activity } from 'lucide-react';

/**
 * Executive Dashboard Example
 *
 * High-level KPIs for leadership with:
 * - Revenue, users, conversion, growth metrics
 * - Trend indicators (up/down)
 * - Comparison to previous period
 * - Revenue trend chart (6 months)
 * - Top products bar chart
 */

interface KPICardProps {
  title: string;
  value: string;
  change: number;
  changeLabel: string;
  icon: React.ReactNode;
  positive?: boolean;
}

function KPICard({ title, value, change, changeLabel, icon, positive = true }: KPICardProps) {
  const isPositive = change >= 0;
  const trendColor = (isPositive && positive) || (!isPositive && !positive) ? '#10b981' : '#ef4444';

  return (
    <div style={{
      backgroundColor: '#fff',
      border: '1px solid #e2e8f0',
      borderRadius: '12px',
      padding: '24px',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ color: '#64748b', fontSize: '14px', fontWeight: 500 }}>{title}</span>
        <div style={{ color: '#94a3b8' }}>{icon}</div>
      </div>

      <div style={{ fontSize: '32px', fontWeight: 700, color: '#0f172a' }}>
        {value}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '14px' }}>
        {isPositive ? (
          <TrendingUp size={16} color={trendColor} />
        ) : (
          <TrendingDown size={16} color={trendColor} />
        )}
        <span style={{ color: trendColor, fontWeight: 600 }}>
          {Math.abs(change)}%
        </span>
        <span style={{ color: '#64748b' }}>{changeLabel}</span>
      </div>
    </div>
  );
}

const revenueData = [
  { month: 'Jul', revenue: 42000 },
  { month: 'Aug', revenue: 45000 },
  { month: 'Sep', revenue: 51000 },
  { month: 'Oct', revenue: 49000 },
  { month: 'Nov', revenue: 58000 },
  { month: 'Dec', revenue: 63000 },
];

const productData = [
  { product: 'Pro Plan', sales: 125000 },
  { product: 'Enterprise', sales: 98000 },
  { product: 'Starter', sales: 67000 },
  { product: 'Add-ons', sales: 34000 },
];

export function ExecutiveDashboard() {
  return (
    <div style={{ padding: '24px', backgroundColor: '#f8fafc', minHeight: '100vh' }}>
      <h1 style={{ fontSize: '30px', fontWeight: 700, marginBottom: '24px', color: '#0f172a' }}>
        Executive Dashboard
      </h1>

      {/* KPI Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <KPICard
          title="Total Revenue"
          value="$63,000"
          change={8.6}
          changeLabel="vs. last month"
          icon={<DollarSign size={24} />}
          positive={true}
        />
        <KPICard
          title="Active Users"
          value="12,543"
          change={12.4}
          changeLabel="vs. last month"
          icon={<Users size={24} />}
          positive={true}
        />
        <KPICard
          title="Conversion Rate"
          value="3.8%"
          change={-2.1}
          changeLabel="vs. last month"
          icon={<ShoppingCart size={24} />}
          positive={true}
        />
        <KPICard
          title="MRR Growth"
          value="18.2%"
          change={5.3}
          changeLabel="vs. last quarter"
          icon={<Activity size={24} />}
          positive={true}
        />
      </div>

      {/* Charts Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '16px',
      }}>
        {/* Revenue Trend */}
        <div style={{
          backgroundColor: '#fff',
          border: '1px solid #e2e8f0',
          borderRadius: '12px',
          padding: '24px',
        }}>
          <h2 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '16px', color: '#0f172a' }}>
            Revenue Trend (6 Months)
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                }}
              />
              <Line
                type="monotone"
                dataKey="revenue"
                stroke="#3b82f6"
                strokeWidth={3}
                dot={{ fill: '#3b82f6', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products */}
        <div style={{
          backgroundColor: '#fff',
          border: '1px solid #e2e8f0',
          borderRadius: '12px',
          padding: '24px',
        }}>
          <h2 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '16px', color: '#0f172a' }}>
            Revenue by Product
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={productData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" stroke="#64748b" />
              <YAxis dataKey="product" type="category" stroke="#64748b" width={100} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                }}
                formatter={(value) => `$${value.toLocaleString()}`}
              />
              <Bar dataKey="sales" fill="#3b82f6" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default ExecutiveDashboard;
