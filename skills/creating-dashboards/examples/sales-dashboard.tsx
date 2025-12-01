/**
 * Sales Analytics Dashboard
 * Complete sales dashboard with revenue KPIs, product charts, and customer tables
 */

import React, { useState, useEffect, useContext } from 'react';
import {
  Card,
  Grid,
  Title,
  Text,
  Metric,
  BadgeDelta,
  AreaChart,
  BarChart,
  DonutChart,
  Table,
  TableHead,
  TableRow,
  TableHeaderCell,
  TableBody,
  TableCell,
  DateRangePicker,
  Select,
  SelectItem,
  MultiSelect,
  MultiSelectItem
} from '@tremor/react';

// Dashboard Context for Global Filters
const DashboardContext = React.createContext({
  filters: {
    dateRange: { start: new Date(), end: new Date() },
    regions: [],
    products: [],
    salesReps: []
  },
  setFilters: () => {},
  refreshInterval: 30000
});

// Main Sales Dashboard Component
export function SalesDashboard() {
  const [filters, setFilters] = useState({
    dateRange: {
      start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      end: new Date()
    },
    regions: [],
    products: [],
    salesReps: []
  });

  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch dashboard data based on filters
  useEffect(() => {
    fetchDashboardData(filters).then(data => {
      setDashboardData(data);
      setLoading(false);
    });
  }, [filters]);

  if (loading) {
    return <DashboardSkeleton />;
  }

  return (
    <DashboardContext.Provider value={{ filters, setFilters, refreshInterval: 30000 }}>
      <div className="p-6 bg-gray-50 min-h-screen">
        {/* Dashboard Header */}
        <div className="mb-6">
          <Title>Sales Analytics Dashboard</Title>
          <Text>Track revenue, products, and customer metrics</Text>
        </div>

        {/* Global Filters */}
        <Card className="mb-6">
          <div className="flex gap-4 flex-wrap">
            <DateRangePicker
              value={filters.dateRange}
              onValueChange={(value) => setFilters({ ...filters, dateRange: value })}
              className="max-w-xs"
            />

            <MultiSelect
              placeholder="Select Regions"
              value={filters.regions}
              onValueChange={(value) => setFilters({ ...filters, regions: value })}
            >
              <MultiSelectItem value="north">North</MultiSelectItem>
              <MultiSelectItem value="south">South</MultiSelectItem>
              <MultiSelectItem value="east">East</MultiSelectItem>
              <MultiSelectItem value="west">West</MultiSelectItem>
            </MultiSelect>

            <MultiSelect
              placeholder="Select Products"
              value={filters.products}
              onValueChange={(value) => setFilters({ ...filters, products: value })}
            >
              <MultiSelectItem value="product-a">Product A</MultiSelectItem>
              <MultiSelectItem value="product-b">Product B</MultiSelectItem>
              <MultiSelectItem value="product-c">Product C</MultiSelectItem>
            </MultiSelect>
          </div>
        </Card>

        {/* KPI Cards */}
        <Grid numItemsSm={2} numItemsLg={4} className="gap-6 mb-6">
          <RevenueKPI data={dashboardData.revenue} />
          <OrdersKPI data={dashboardData.orders} />
          <CustomersKPI data={dashboardData.customers} />
          <ConversionKPI data={dashboardData.conversion} />
        </Grid>

        {/* Charts Row */}
        <Grid numItemsLg={2} className="gap-6 mb-6">
          <RevenueChart data={dashboardData.revenueHistory} />
          <ProductPerformance data={dashboardData.products} />
        </Grid>

        {/* Sales by Region and Top Products */}
        <Grid numItemsLg={3} className="gap-6 mb-6">
          <RegionalSales data={dashboardData.regions} />
          <TopProducts data={dashboardData.topProducts} />
          <SalesTeamPerformance data={dashboardData.salesTeam} />
        </Grid>

        {/* Recent Transactions Table */}
        <Card>
          <Title>Recent Transactions</Title>
          <TransactionsTable data={dashboardData.transactions} />
        </Card>
      </div>
    </DashboardContext.Provider>
  );
}

// KPI Components
function RevenueKPI({ data }) {
  return (
    <Card>
      <Text>Total Revenue</Text>
      <Metric>${data.value.toLocaleString()}</Metric>
      <div className="flex items-center justify-between mt-4">
        <BadgeDelta deltaType={data.trend > 0 ? 'increase' : 'decrease'}>
          {data.trend > 0 ? '+' : ''}{data.trend}%
        </BadgeDelta>
        <Text className="text-xs">vs last period</Text>
      </div>
      <Sparkline data={data.sparkline} className="mt-4 h-10" />
    </Card>
  );
}

function OrdersKPI({ data }) {
  return (
    <Card>
      <Text>Total Orders</Text>
      <Metric>{data.value.toLocaleString()}</Metric>
      <div className="flex items-center justify-between mt-4">
        <BadgeDelta deltaType={data.trend > 0 ? 'increase' : 'decrease'}>
          {data.trend > 0 ? '+' : ''}{data.trend}%
        </BadgeDelta>
        <Text className="text-xs">vs last period</Text>
      </div>
    </Card>
  );
}

function CustomersKPI({ data }) {
  return (
    <Card>
      <Text>New Customers</Text>
      <Metric>{data.value.toLocaleString()}</Metric>
      <div className="flex items-center justify-between mt-4">
        <BadgeDelta deltaType={data.trend > 0 ? 'increase' : 'decrease'}>
          {data.trend > 0 ? '+' : ''}{data.trend}%
        </BadgeDelta>
        <Text className="text-xs">vs last period</Text>
      </div>
    </Card>
  );
}

function ConversionKPI({ data }) {
  return (
    <Card>
      <Text>Conversion Rate</Text>
      <Metric>{data.value}%</Metric>
      <div className="flex items-center justify-between mt-4">
        <BadgeDelta deltaType={data.trend > 0 ? 'increase' : 'decrease'}>
          {data.trend > 0 ? '+' : ''}{data.trend} pp
        </BadgeDelta>
        <Text className="text-xs">vs last period</Text>
      </div>
      <ProgressBar value={data.value} className="mt-4" />
    </Card>
  );
}

// Chart Components
function RevenueChart({ data }) {
  const { filters } = useContext(DashboardContext);

  return (
    <Card>
      <Title>Revenue Trend</Title>
      <Text>Daily revenue over selected period</Text>
      <AreaChart
        className="h-72 mt-4"
        data={data}
        index="date"
        categories={["revenue", "target"]}
        colors={["blue", "gray"]}
        valueFormatter={(value) => `$${(value / 1000).toFixed(1)}k`}
        showLegend
        showGridLines
        showAnimation
      />
    </Card>
  );
}

function ProductPerformance({ data }) {
  return (
    <Card>
      <Title>Product Performance</Title>
      <Text>Revenue by product category</Text>
      <BarChart
        className="h-72 mt-4"
        data={data}
        index="product"
        categories={["revenue", "units"]}
        colors={["blue", "cyan"]}
        valueFormatter={(value) => `$${(value / 1000).toFixed(1)}k`}
        showLegend
        stack={false}
      />
    </Card>
  );
}

function RegionalSales({ data }) {
  return (
    <Card>
      <Title>Sales by Region</Title>
      <DonutChart
        className="h-60 mt-4"
        data={data}
        category="sales"
        index="region"
        valueFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
        colors={["blue", "cyan", "indigo", "violet"]}
        showLabel
        showAnimation
      />
      <div className="mt-4">
        {data.map((item) => (
          <div key={item.region} className="flex justify-between py-1">
            <Text>{item.region}</Text>
            <Text className="font-medium">${(item.sales / 1000).toFixed(0)}k</Text>
          </div>
        ))}
      </div>
    </Card>
  );
}

function TopProducts({ data }) {
  return (
    <Card>
      <Title>Top Products</Title>
      <Table className="mt-4">
        <TableHead>
          <TableRow>
            <TableHeaderCell>Product</TableHeaderCell>
            <TableHeaderCell>Revenue</TableHeaderCell>
            <TableHeaderCell>Growth</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.slice(0, 5).map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.name}</TableCell>
              <TableCell>${(item.revenue / 1000).toFixed(1)}k</TableCell>
              <TableCell>
                <BadgeDelta deltaType={item.growth > 0 ? 'increase' : 'decrease'}>
                  {item.growth}%
                </BadgeDelta>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}

function SalesTeamPerformance({ data }) {
  return (
    <Card>
      <Title>Sales Team Performance</Title>
      <div className="mt-4 space-y-4">
        {data.slice(0, 5).map((rep) => (
          <div key={rep.id}>
            <div className="flex justify-between mb-1">
              <Text>{rep.name}</Text>
              <Text className="font-medium">${(rep.sales / 1000).toFixed(0)}k</Text>
            </div>
            <ProgressBar value={(rep.sales / rep.target) * 100} color="blue" />
            <Text className="text-xs mt-1">{((rep.sales / rep.target) * 100).toFixed(0)}% of target</Text>
          </div>
        ))}
      </div>
    </Card>
  );
}

// Transactions Table
function TransactionsTable({ data }) {
  const [page, setPage] = useState(0);
  const pageSize = 10;

  const paginatedData = data.slice(page * pageSize, (page + 1) * pageSize);

  return (
    <>
      <Table className="mt-4">
        <TableHead>
          <TableRow>
            <TableHeaderCell>Transaction ID</TableHeaderCell>
            <TableHeaderCell>Date</TableHeaderCell>
            <TableHeaderCell>Customer</TableHeaderCell>
            <TableHeaderCell>Product</TableHeaderCell>
            <TableHeaderCell>Amount</TableHeaderCell>
            <TableHeaderCell>Status</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {paginatedData.map((transaction) => (
            <TableRow key={transaction.id}>
              <TableCell>{transaction.id}</TableCell>
              <TableCell>{new Date(transaction.date).toLocaleDateString()}</TableCell>
              <TableCell>{transaction.customer}</TableCell>
              <TableCell>{transaction.product}</TableCell>
              <TableCell>${transaction.amount.toLocaleString()}</TableCell>
              <TableCell>
                <Badge color={transaction.status === 'completed' ? 'green' : 'yellow'}>
                  {transaction.status}
                </Badge>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-4">
        <Text>
          Showing {page * pageSize + 1} to {Math.min((page + 1) * pageSize, data.length)} of {data.length}
        </Text>
        <div className="flex gap-2">
          <button
            onClick={() => setPage(Math.max(0, page - 1))}
            disabled={page === 0}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <button
            onClick={() => setPage(page + 1)}
            disabled={(page + 1) * pageSize >= data.length}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </>
  );
}

// Loading Skeleton
function DashboardSkeleton() {
  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-6"></div>

        <Grid numItemsLg={4} className="gap-6 mb-6">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/3"></div>
            </Card>
          ))}
        </Grid>
      </div>
    </div>
  );
}

// Sparkline Component
function Sparkline({ data, className = '' }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;

  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * 100;
    const y = 100 - ((value - min) / range) * 100;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg className={`w-full ${className}`} viewBox="0 0 100 100" preserveAspectRatio="none">
      <polyline
        points={points}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        className="text-blue-500"
      />
    </svg>
  );
}

// Badge Component
function Badge({ children, color = 'gray' }) {
  const colors = {
    green: 'bg-green-100 text-green-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    red: 'bg-red-100 text-red-800',
    gray: 'bg-gray-100 text-gray-800'
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded ${colors[color]}`}>
      {children}
    </span>
  );
}

// Progress Bar Component
function ProgressBar({ value, color = 'blue', className = '' }) {
  return (
    <div className={`w-full bg-gray-200 rounded-full h-2 ${className}`}>
      <div
        className={`h-2 rounded-full bg-${color}-500`}
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}

// Mock data fetching function
async function fetchDashboardData(filters) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000));

  return {
    revenue: {
      value: 1245832,
      trend: 15.3,
      sparkline: [100, 120, 115, 140, 155, 145, 160, 180, 175, 190, 210, 205]
    },
    orders: {
      value: 3421,
      trend: 8.7
    },
    customers: {
      value: 892,
      trend: -2.3
    },
    conversion: {
      value: 3.8,
      trend: 0.5
    },
    revenueHistory: generateRevenueHistory(),
    products: generateProductData(),
    regions: generateRegionalData(),
    topProducts: generateTopProducts(),
    salesTeam: generateSalesTeamData(),
    transactions: generateTransactions()
  };
}

// Data generation helpers
function generateRevenueHistory() {
  const data = [];
  const now = new Date();

  for (let i = 30; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);

    data.push({
      date: date.toISOString().split('T')[0],
      revenue: Math.floor(Math.random() * 50000) + 30000,
      target: 40000
    });
  }

  return data;
}

function generateProductData() {
  return [
    { product: 'Product A', revenue: 125000, units: 1250 },
    { product: 'Product B', revenue: 98000, units: 890 },
    { product: 'Product C', revenue: 87000, units: 1100 },
    { product: 'Product D', revenue: 65000, units: 450 }
  ];
}

function generateRegionalData() {
  return [
    { region: 'North', sales: 425000 },
    { region: 'South', sales: 380000 },
    { region: 'East', sales: 290000 },
    { region: 'West', sales: 150832 }
  ];
}

function generateTopProducts() {
  return [
    { id: 1, name: 'Premium Widget', revenue: 234000, growth: 23.5 },
    { id: 2, name: 'Standard Widget', revenue: 189000, growth: 15.2 },
    { id: 3, name: 'Basic Widget', revenue: 145000, growth: 8.7 },
    { id: 4, name: 'Deluxe Widget', revenue: 98000, growth: -5.3 },
    { id: 5, name: 'Compact Widget', revenue: 87000, growth: 12.1 }
  ];
}

function generateSalesTeamData() {
  return [
    { id: 1, name: 'John Smith', sales: 145000, target: 150000 },
    { id: 2, name: 'Jane Doe', sales: 132000, target: 140000 },
    { id: 3, name: 'Mike Johnson', sales: 118000, target: 130000 },
    { id: 4, name: 'Sarah Williams', sales: 105000, target: 120000 },
    { id: 5, name: 'Tom Brown', sales: 95000, target: 110000 }
  ];
}

function generateTransactions() {
  const transactions = [];
  const products = ['Widget A', 'Widget B', 'Widget C', 'Widget D'];
  const customers = ['Acme Corp', 'GlobalTech', 'MegaCorp', 'TechStart', 'Enterprise Inc'];
  const statuses = ['completed', 'pending', 'completed', 'completed'];

  for (let i = 0; i < 50; i++) {
    transactions.push({
      id: `TRX-${1000 + i}`,
      date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000),
      customer: customers[Math.floor(Math.random() * customers.length)],
      product: products[Math.floor(Math.random() * products.length)],
      amount: Math.floor(Math.random() * 5000) + 500,
      status: statuses[Math.floor(Math.random() * statuses.length)]
    });
  }

  return transactions.sort((a, b) => b.date - a.date);
}

export default SalesDashboard;