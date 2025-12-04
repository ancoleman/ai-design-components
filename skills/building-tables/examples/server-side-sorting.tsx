import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react';

/**
 * Server-Side Sorting and Filtering Example
 *
 * For large datasets (100K+ rows), perform sorting/filtering on the server.
 * Frontend sends sort/filter parameters, backend returns paginated results.
 *
 * API format: GET /api/users?page=1&pageSize=20&sortBy=name&sortOrder=asc&filter={"role":"admin"}
 */

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  createdAt: string;
}

interface TableState {
  page: number;
  pageSize: number;
  sortBy: string | null;
  sortOrder: 'asc' | 'desc';
  filters: Record<string, string>;
}

async function fetchUsers(state: TableState) {
  const params = new URLSearchParams({
    page: state.page.toString(),
    pageSize: state.pageSize.toString(),
    ...(state.sortBy && { sortBy: state.sortBy, sortOrder: state.sortOrder }),
    ...(Object.keys(state.filters).length && { filter: JSON.stringify(state.filters) }),
  });

  const response = await fetch(`/api/users?${params}`);
  return response.json();
}

export function ServerSideSortingTable() {
  const [tableState, setTableState] = useState<TableState>({
    page: 1,
    pageSize: 20,
    sortBy: null,
    sortOrder: 'asc',
    filters: {},
  });

  const { data, isLoading } = useQuery({
    queryKey: ['users', tableState],
    queryFn: () => fetchUsers(tableState),
    keepPreviousData: true,  // Show old data while fetching new
  });

  const handleSort = (column: string) => {
    setTableState((prev) => ({
      ...prev,
      sortBy: column,
      sortOrder: prev.sortBy === column && prev.sortOrder === 'asc' ? 'desc' : 'asc',
      page: 1,  // Reset to first page on sort
    }));
  };

  const handleFilter = (column: string, value: string) => {
    setTableState((prev) => ({
      ...prev,
      filters: value ? { ...prev.filters, [column]: value } : { ...prev.filters, [column]: undefined },
      page: 1,  // Reset to first page on filter
    }));
  };

  const SortIcon = ({ column }: { column: string }) => {
    if (tableState.sortBy !== column) {
      return <ChevronsUpDown size={14} className="text-gray-400" />;
    }
    return tableState.sortOrder === 'asc' ? (
      <ChevronUp size={14} className="text-blue-600" />
    ) : (
      <ChevronDown size={14} className="text-blue-600" />
    );
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Server-Side Table (100K+ rows)</h1>

      <div className="mb-4 p-3 bg-yellow-50 rounded-lg text-sm text-yellow-900">
        ℹ️ Sorting and filtering performed on server. Efficient for large datasets.
      </div>

      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              {['name', 'email', 'role', 'createdAt'].map((col) => (
                <th key={col} className="px-6 py-3 text-left">
                  <div
                    onClick={() => handleSort(col)}
                    className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 -mx-2 px-2 py-1 rounded"
                  >
                    <span className="text-xs font-medium text-gray-500 uppercase">
                      {col}
                    </span>
                    <SortIcon column={col} />
                  </div>

                  {/* Column filter */}
                  <input
                    type="text"
                    placeholder={`Filter ${col}...`}
                    value={tableState.filters[col] || ''}
                    onChange={(e) => handleFilter(col, e.target.value)}
                    onClick={(e) => e.stopPropagation()}
                    className="mt-2 px-2 py-1 text-xs border rounded w-full"
                  />
                </th>
              ))}
            </tr>
          </thead>

          <tbody className="bg-white divide-y">
            {isLoading ? (
              // Loading skeleton
              Array.from({ length: 5 }).map((_, i) => (
                <tr key={i}>
                  {Array.from({ length: 4 }).map((_, j) => (
                    <td key={j} className="px-6 py-4">
                      <div className="h-4 bg-gray-200 rounded animate-pulse" />
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              data?.users.map((user: User) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium">{user.name}</td>
                  <td className="px-6 py-4 text-gray-600">{user.email}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{user.createdAt}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 flex justify-between items-center">
        <div className="text-sm text-gray-700">
          Showing page {tableState.page} of {data?.totalPages || 1} ({data?.totalCount || 0} total)
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setTableState({ ...tableState, page: Math.max(1, tableState.page - 1) })}
            disabled={tableState.page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Previous
          </button>

          <button
            onClick={() => setTableState({ ...tableState, page: tableState.page + 1 })}
            disabled={tableState.page >= (data?.totalPages || 1)}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default ServerSideSortingTable;
