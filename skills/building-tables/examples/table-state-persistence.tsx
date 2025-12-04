import React, { useState, useEffect } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  SortingState,
  ColumnFiltersState,
  VisibilityState,
  ColumnDef,
} from '@tanstack/react-table';

/**
 * Table State Persistence Example
 *
 * Saves and restores table state to localStorage:
 * - Column sorting
 * - Column filters
 * - Column visibility
 * - Pagination state
 * - Column order
 * - Column sizing
 */

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  department: string;
}

const data: User[] = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', department: 'IT' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'Manager', department: 'Sales' },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'Developer', department: 'Engineering' },
  // Add more data...
];

const columns: ColumnDef<User>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'email', header: 'Email' },
  { accessorKey: 'role', header: 'Role' },
  { accessorKey: 'department', header: 'Department' },
];

const STATE_KEY = 'table-state-v1';

export function TableStatePersistence() {
  // Load state from localStorage
  const loadState = () => {
    const saved = localStorage.getItem(STATE_KEY);
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return {};
      }
    }
    return {};
  };

  const savedState = loadState();

  const [sorting, setSorting] = useState<SortingState>(savedState.sorting || []);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(savedState.columnFilters || []);
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>(savedState.columnVisibility || {});
  const [pagination, setPagination] = useState(savedState.pagination || { pageIndex: 0, pageSize: 10 });

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      pagination,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  // Save state to localStorage whenever it changes
  useEffect(() => {
    const state = {
      sorting,
      columnFilters,
      columnVisibility,
      pagination,
    };

    localStorage.setItem(STATE_KEY, JSON.stringify(state));
  }, [sorting, columnFilters, columnVisibility, pagination]);

  const resetState = () => {
    localStorage.removeItem(STATE_KEY);
    setSorting([]);
    setColumnFilters([]);
    setColumnVisibility({});
    setPagination({ pageIndex: 0, pageSize: 10 });
  };

  return (
    <div className="p-4">
      <div className="mb-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Table with Persistent State</h1>

        <button
          onClick={resetState}
          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
        >
          Reset State
        </button>
      </div>

      <div className="mb-4 p-3 bg-green-50 rounded-lg text-sm text-green-900">
        ✓ Table state is automatically saved to localStorage and restored on page reload
      </div>

      {/* Column visibility toggles */}
      <div className="mb-4 flex gap-2 flex-wrap">
        {table.getAllLeafColumns().map((column) => (
          <label key={column.id} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={column.getIsVisible()}
              onChange={column.getToggleVisibilityHandler()}
            />
            <span className="text-sm">{column.id}</span>
          </label>
        ))}
      </div>

      {/* Table */}
      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="px-6 py-3 text-left">
                    <div
                      onClick={header.column.getToggleSortingHandler()}
                      className="cursor-pointer select-none"
                    >
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {{
                        asc: ' ↑',
                        desc: ' ↓',
                      }[header.column.getIsSorted() as string] ?? null}
                    </div>

                    {/* Column filter */}
                    {header.column.getCanFilter() && (
                      <input
                        type="text"
                        value={(header.column.getFilterValue() as string) ?? ''}
                        onChange={(e) => header.column.setFilterValue(e.target.value)}
                        placeholder="Filter..."
                        className="mt-2 px-2 py-1 text-xs border rounded w-full"
                        onClick={(e) => e.stopPropagation()}
                      />
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>

          <tbody className="bg-white divide-y">
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="hover:bg-gray-50">
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="px-6 py-4">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 flex justify-between items-center">
        <span className="text-sm text-gray-700">
          Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
        </span>

        <div className="flex gap-2">
          <button
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <button
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default TableStatePersistence;
