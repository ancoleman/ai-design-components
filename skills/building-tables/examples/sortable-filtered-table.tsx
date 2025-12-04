import React, { useState, useMemo } from 'react';
import { ChevronUp, ChevronDown, Filter } from 'lucide-react';

/**
 * Sortable and Filterable Table Example
 *
 * Features:
 * - Multi-column sorting
 * - Per-column filters
 * - Global search
 * - Filter chips
 * - Clear all filters
 */

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
  status: 'In Stock' | 'Low Stock' | 'Out of Stock';
}

const products: Product[] = [
  { id: 1, name: 'Laptop Pro', category: 'Electronics', price: 1299, stock: 15, status: 'In Stock' },
  { id: 2, name: 'Wireless Mouse', category: 'Accessories', price: 29, stock: 3, status: 'Low Stock' },
  { id: 3, name: 'Keyboard', category: 'Accessories', price: 79, stock: 0, status: 'Out of Stock' },
  { id: 4, name: 'Monitor 27"', category: 'Electronics', price: 399, stock: 8, status: 'In Stock' },
  { id: 5, name: 'USB-C Hub', category: 'Accessories', price: 49, stock: 25, status: 'In Stock' },
];

export function SortableFilteredTable() {
  const [sortColumn, setSortColumn] = useState<keyof Product | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [filters, setFilters] = useState({
    category: '',
    status: '',
    search: '',
  });

  const handleSort = (column: keyof Product) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedData = useMemo(() => {
    let result = [...products];

    // Apply filters
    if (filters.category) {
      result = result.filter((p) => p.category === filters.category);
    }
    if (filters.status) {
      result = result.filter((p) => p.status === filters.status);
    }
    if (filters.search) {
      result = result.filter((p) =>
        p.name.toLowerCase().includes(filters.search.toLowerCase())
      );
    }

    // Apply sorting
    if (sortColumn) {
      result.sort((a, b) => {
        const aVal = a[sortColumn];
        const bVal = b[sortColumn];

        if (sortDirection === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
    }

    return result;
  }, [filters, sortColumn, sortDirection]);

  const clearFilters = () => {
    setFilters({ category: '', status: '', search: '' });
  };

  const activeFilterCount = Object.values(filters).filter(Boolean).length;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Product Inventory</h1>

      {/* Filters */}
      <div className="mb-4 flex gap-4 flex-wrap">
        <input
          type="text"
          placeholder="Search products..."
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          className="px-4 py-2 border rounded-lg w-64"
        />

        <select
          value={filters.category}
          onChange={(e) => setFilters({ ...filters, category: e.target.value })}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="">All Categories</option>
          <option value="Electronics">Electronics</option>
          <option value="Accessories">Accessories</option>
        </select>

        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="">All Status</option>
          <option value="In Stock">In Stock</option>
          <option value="Low Stock">Low Stock</option>
          <option value="Out of Stock">Out of Stock</option>
        </select>

        {activeFilterCount > 0 && (
          <button
            onClick={clearFilters}
            className="px-4 py-2 text-blue-600 hover:text-blue-800"
          >
            Clear Filters ({activeFilterCount})
          </button>
        )}
      </div>

      {/* Results count */}
      <div className="mb-2 text-sm text-gray-600">
        Showing {filteredAndSortedData.length} of {products.length} products
      </div>

      {/* Table */}
      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              {(['name', 'category', 'price', 'stock', 'status'] as const).map((col) => (
                <th
                  key={col}
                  onClick={() => handleSort(col)}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center gap-2">
                    {col}
                    {sortColumn === col && (
                      sortDirection === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          <tbody className="bg-white divide-y">
            {filteredAndSortedData.map((product) => (
              <tr key={product.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">{product.name}</td>
                <td className="px-6 py-4">{product.category}</td>
                <td className="px-6 py-4">${product.price}</td>
                <td className="px-6 py-4">{product.stock}</td>
                <td className="px-6 py-4">
                  <span
                    className={`px-2 py-1 rounded text-xs ${
                      product.status === 'In Stock'
                        ? 'bg-green-100 text-green-800'
                        : product.status === 'Low Stock'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {product.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default SortableFilteredTable;
