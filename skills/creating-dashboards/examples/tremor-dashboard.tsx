import { Card, Title, Text, Metric, Flex, BadgeDelta, AreaChart, BarList } from '@tremor/react';

/**
 * Tremor Dashboard Example
 *
 * Uses Tremor library for pre-built dashboard components.
 * Tremor provides beautiful, accessible components out-of-the-box.
 *
 * Install: npm install @tremor/react
 */

const salesData = [
  { month: 'Jan', Sales: 4500, Target: 4000 },
  { month: 'Feb', Sales: 3800, Target: 4000 },
  { month: 'Mar', Sales: 5100, Target: 4500 },
  { month: 'Apr', Sales: 4600, Target: 4500 },
  { month: 'May', Sales: 5400, Target: 5000 },
  { month: 'Jun', Sales: 6200, Target: 5500 },
];

const topProducts = [
  { name: 'Pro Plan', value: 45000 },
  { name: 'Enterprise', value: 38000 },
  { name: 'Starter', value: 29000 },
  { name: 'Add-ons', value: 12000 },
];

export function TremorDashboard() {
  return (
    <div style={{ padding: '24px', backgroundColor: '#f9fafb', minHeight: '100vh' }}>
      <Title>Sales Dashboard</Title>
      <Text>Overview of sales performance and key metrics</Text>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px', marginTop: '24px' }}>
        <Card>
          <Flex alignItems="start">
            <div>
              <Text>Revenue</Text>
              <Metric>$63,000</Metric>
            </div>
            <BadgeDelta deltaType="increase">8.6%</BadgeDelta>
          </Flex>
        </Card>

        <Card>
          <Flex alignItems="start">
            <div>
              <Text>Active Users</Text>
              <Metric>12,543</Metric>
            </div>
            <BadgeDelta deltaType="increase">12.4%</BadgeDelta>
          </Flex>
        </Card>

        <Card>
          <Flex alignItems="start">
            <div>
              <Text>Conversion Rate</Text>
              <Metric>3.8%</Metric>
            </div>
            <BadgeDelta deltaType="decrease">-2.1%</BadgeDelta>
          </Flex>
        </Card>
      </div>

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '16px', marginTop: '24px' }}>
        <Card>
          <Title>Sales vs Target</Title>
          <AreaChart
            className="mt-4 h-72"
            data={salesData}
            index="month"
            categories={['Sales', 'Target']}
            colors={['blue', 'gray']}
            valueFormatter={(number) => `$${(number / 1000).toFixed(1)}K`}
            yAxisWidth={48}
          />
        </Card>

        <Card>
          <Title>Top Products</Title>
          <Flex className="mt-4">
            <Text>Product</Text>
            <Text>Revenue</Text>
          </Flex>
          <BarList
            data={topProducts}
            className="mt-2"
            valueFormatter={(number) => `$${(number / 1000).toFixed(0)}K`}
          />
        </Card>
      </div>
    </div>
  );
}

export default TremorDashboard;
