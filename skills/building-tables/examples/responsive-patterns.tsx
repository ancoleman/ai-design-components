import React from 'react';

/**
 * Responsive Table Patterns Comparison
 *
 * Demonstrates 3 different responsive strategies:
 * 1. Horizontal scroll
 * 2. Priority columns (hide less important on mobile)
 * 3. Card layout transformation
 */

interface Order {
  id: number;
  customer: string;
  product: string;
  amount: number;
  status: string;
  date: string;
}

const orders: Order[] = [
  { id: 1001, customer: 'John Doe', product: 'Laptop Pro', amount: 1299, status: 'Shipped', date: '2025-12-01' },
  { id: 1002, customer: 'Jane Smith', product: 'Mouse', amount: 29, status: 'Processing', date: '2025-12-02' },
  { id: 1003, customer: 'Bob Johnson', product: 'Monitor', amount: 399, status: 'Delivered', date: '2025-12-03' },
];

// Pattern 1: Horizontal Scroll
function HorizontalScrollTable() {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Pattern 1: Horizontal Scroll</h2>
      <div className="overflow-x-auto border rounded-lg">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left">Order ID</th>
              <th className="px-6 py-3 text-left">Customer</th>
              <th className="px-6 py-3 text-left">Product</th>
              <th className="px-6 py-3 text-left">Amount</th>
              <th className="px-6 py-3 text-left">Status</th>
              <th className="px-6 py-3 text-left">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {orders.map((order) => (
              <tr key={order.id}>
                <td className="px-6 py-4">{order.id}</td>
                <td className="px-6 py-4">{order.customer}</td>
                <td className="px-6 py-4">{order.product}</td>
                <td className="px-6 py-4">${order.amount}</td>
                <td className="px-6 py-4">{order.status}</td>
                <td className="px-6 py-4">{order.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-sm text-gray-600 mt-2">✓ Simple | ✗ Poor mobile UX (horizontal scroll)</p>
    </div>
  );
}

// Pattern 2: Priority Columns
function PriorityColumnsTable() {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Pattern 2: Priority Columns</h2>
      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left">Order ID</th>
              <th className="px-6 py-3 text-left">Customer</th>
              <th className="px-6 py-3 text-left hidden md:table-cell">Product</th>
              <th className="px-6 py-3 text-left">Amount</th>
              <th className="px-6 py-3 text-left hidden lg:table-cell">Status</th>
              <th className="px-6 py-3 text-left hidden lg:table-cell">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {orders.map((order) => (
              <tr key={order.id}>
                <td className="px-6 py-4">{order.id}</td>
                <td className="px-6 py-4">{order.customer}</td>
                <td className="px-6 py-4 hidden md:table-cell">{order.product}</td>
                <td className="px-6 py-4 font-semibold">${order.amount}</td>
                <td className="px-6 py-4 hidden lg:table-cell">{order.status}</td>
                <td className="px-6 py-4 hidden lg:table-cell">{order.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-sm text-gray-600 mt-2">
        ✓ Moderate complexity | ✓ Shows most important columns | ✗ Hidden data not accessible
      </p>
    </div>
  );
}

// Pattern 3: Card Layout
function CardLayoutTable() {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Pattern 3: Card Layout (Mobile-Optimized)</h2>

      <div className="space-y-4 md:hidden">
        {orders.map((order) => (
          <div key={order.id} className="border rounded-lg p-4 bg-white">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs text-gray-500">Order #{order.id}</span>
              <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                {order.status}
              </span>
            </div>

            <h3 className="font-semibold text-lg mb-1">{order.customer}</h3>
            <p className="text-sm text-gray-600 mb-2">{order.product}</p>

            <div className="flex justify-between items-center pt-2 border-t">
              <span className="font-bold text-lg text-blue-600">${order.amount}</span>
              <span className="text-sm text-gray-500">{order.date}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="hidden md:block overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left">Order ID</th>
              <th className="px-6 py-3 text-left">Customer</th>
              <th className="px-6 py-3 text-left">Product</th>
              <th className="px-6 py-3 text-left">Amount</th>
              <th className="px-6 py-3 text-left">Status</th>
              <th className="px-6 py-3 text-left">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {orders.map((order) => (
              <tr key={order.id}>
                <td className="px-6 py-4">{order.id}</td>
                <td className="px-6 py-4">{order.customer}</td>
                <td className="px-6 py-4">{order.product}</td>
                <td className="px-6 py-4">${order.amount}</td>
                <td className="px-6 py-4">{order.status}</td>
                <td className="px-6 py-4">{order.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-sm text-gray-600 mt-2">
        ✓ Best mobile UX | ✓ All data accessible | ✗ More code complexity
      </p>
    </div>
  );
}

export function ResponsivePatternsComparison() {
  return (
    <div className="p-4 space-y-8">
      <div>
        <h1 className="text-2xl font-bold mb-2">Responsive Table Patterns</h1>
        <p className="text-gray-600 mb-6">
          Resize your browser to see how each pattern adapts to mobile screens.
        </p>
      </div>

      <HorizontalScrollTable />
      <PriorityColumnsTable />
      <CardLayoutTable />

      <div className="mt-8 p-4 bg-gray-100 rounded-lg">
        <h3 className="font-semibold mb-2">Recommendation:</h3>
        <ul className="text-sm space-y-1 text-gray-700">
          <li>• <strong>Quick implementation:</strong> Horizontal scroll</li>
          <li>• <strong>Moderate columns (5-8):</strong> Priority columns</li>
          <li>• <strong>Many columns (8+) or mobile-first:</strong> Card layout</li>
          <li>• <strong>Enterprise apps:</strong> AG Grid responsive features</li>
        </ul>
      </div>
    </div>
  );
}

export default ResponsivePatternsComparison;
