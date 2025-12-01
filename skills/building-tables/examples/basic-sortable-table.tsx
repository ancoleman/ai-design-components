import React, { useState, useMemo } from 'react';

/**
 * Basic Sortable Table Example
 * Demonstrates client-side sorting for small datasets (<100 rows)
 */

interface Person {
  id: number;
  name: string;
  email: string;
  department: string;
  salary: number;
  startDate: string;
}

interface SortConfig {
  key: keyof Person | null;
  direction: 'ascending' | 'descending';
}

const BasicSortableTable: React.FC = () => {
  // Sample data
  const data: Person[] = [
    { id: 1, name: 'Alice Johnson', email: 'alice@example.com', department: 'Engineering', salary: 95000, startDate: '2021-03-15' },
    { id: 2, name: 'Bob Smith', email: 'bob@example.com', department: 'Sales', salary: 75000, startDate: '2020-07-22' },
    { id: 3, name: 'Charlie Brown', email: 'charlie@example.com', department: 'Marketing', salary: 82000, startDate: '2022-01-10' },
    { id: 4, name: 'Diana Prince', email: 'diana@example.com', department: 'Engineering', salary: 105000, startDate: '2019-11-05' },
    { id: 5, name: 'Edward Norton', email: 'edward@example.com', department: 'HR', salary: 68000, startDate: '2021-09-20' },
  ];

  const [sortConfig, setSortConfig] = useState<SortConfig>({
    key: null,
    direction: 'ascending'
  });

  // Handle sort click
  const handleSort = (key: keyof Person) => {
    let direction: 'ascending' | 'descending' = 'ascending';

    if (sortConfig.key === key) {
      if (sortConfig.direction === 'ascending') {
        direction = 'descending';
      } else {
        // Reset sort on third click
        setSortConfig({ key: null, direction: 'ascending' });
        return;
      }
    }

    setSortConfig({ key, direction });
  };

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return data;

    return [...data].sort((a, b) => {
      const aValue = a[sortConfig.key as keyof Person];
      const bValue = b[sortConfig.key as keyof Person];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;
      if (aValue === bValue) return 0;

      // Handle different data types
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortConfig.direction === 'ascending'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      // Numeric and date comparison
      const comparison = aValue > bValue ? 1 : -1;
      return sortConfig.direction === 'ascending' ? comparison : -comparison;
    });
  }, [data, sortConfig]);

  // Get sort indicator
  const getSortIndicator = (column: keyof Person) => {
    if (sortConfig.key !== column) return <span className="sort-indicator">↕️</span>;
    return sortConfig.direction === 'ascending'
      ? <span className="sort-indicator">↑</span>
      : <span className="sort-indicator">↓</span>;
  };

  // Format currency
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="table-container">
      <h2>Employee Directory</h2>

      <table className="sortable-table" role="table">
        <caption>
          Click column headers to sort. Click again to reverse order.
        </caption>

        <thead>
          <tr>
            <th
              scope="col"
              onClick={() => handleSort('name')}
              className="sortable"
              aria-sort={
                sortConfig.key === 'name'
                  ? sortConfig.direction === 'ascending'
                    ? 'ascending'
                    : 'descending'
                  : 'none'
              }
            >
              Name {getSortIndicator('name')}
            </th>

            <th
              scope="col"
              onClick={() => handleSort('email')}
              className="sortable"
              aria-sort={
                sortConfig.key === 'email'
                  ? sortConfig.direction === 'ascending'
                    ? 'ascending'
                    : 'descending'
                  : 'none'
              }
            >
              Email {getSortIndicator('email')}
            </th>

            <th
              scope="col"
              onClick={() => handleSort('department')}
              className="sortable"
              aria-sort={
                sortConfig.key === 'department'
                  ? sortConfig.direction === 'ascending'
                    ? 'ascending'
                    : 'descending'
                  : 'none'
              }
            >
              Department {getSortIndicator('department')}
            </th>

            <th
              scope="col"
              onClick={() => handleSort('salary')}
              className="sortable align-right"
              aria-sort={
                sortConfig.key === 'salary'
                  ? sortConfig.direction === 'ascending'
                    ? 'ascending'
                    : 'descending'
                  : 'none'
              }
            >
              Salary {getSortIndicator('salary')}
            </th>

            <th
              scope="col"
              onClick={() => handleSort('startDate')}
              className="sortable"
              aria-sort={
                sortConfig.key === 'startDate'
                  ? sortConfig.direction === 'ascending'
                    ? 'ascending'
                    : 'descending'
                  : 'none'
              }
            >
              Start Date {getSortIndicator('startDate')}
            </th>
          </tr>
        </thead>

        <tbody>
          {sortedData.map((person) => (
            <tr key={person.id}>
              <td>{person.name}</td>
              <td>
                <a href={`mailto:${person.email}`}>{person.email}</a>
              </td>
              <td>{person.department}</td>
              <td className="align-right">{formatCurrency(person.salary)}</td>
              <td>{formatDate(person.startDate)}</td>
            </tr>
          ))}
        </tbody>

        <tfoot>
          <tr>
            <td colSpan={5} className="summary">
              Showing {sortedData.length} employees
              {sortConfig.key && (
                <span>
                  {' '}• Sorted by {sortConfig.key} ({sortConfig.direction})
                </span>
              )}
            </td>
          </tr>
        </tfoot>
      </table>

      <style jsx>{`
        .table-container {
          max-width: 1200px;
          margin: 2rem auto;
          padding: 0 1rem;
          font-family: system-ui, -apple-system, sans-serif;
        }

        h2 {
          margin-bottom: 1rem;
          color: var(--color-text-primary, #1a1a1a);
        }

        table {
          width: 100%;
          border-collapse: collapse;
          background: white;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          border-radius: 8px;
          overflow: hidden;
        }

        caption {
          padding: 0.75rem;
          text-align: left;
          font-style: italic;
          color: var(--color-text-secondary, #666);
          font-size: 0.875rem;
        }

        th {
          background: var(--table-header-bg, #f8f9fa);
          padding: 0.75rem 1rem;
          text-align: left;
          font-weight: 600;
          color: var(--table-header-text, #495057);
          border-bottom: 2px solid var(--table-border, #dee2e6);
          position: relative;
          user-select: none;
        }

        th.sortable {
          cursor: pointer;
          transition: background-color 0.2s;
        }

        th.sortable:hover {
          background: var(--table-header-hover, #e9ecef);
        }

        .sort-indicator {
          margin-left: 0.5rem;
          display: inline-block;
          opacity: 0.7;
          font-size: 0.875em;
        }

        td {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--table-border, #dee2e6);
        }

        tbody tr {
          transition: background-color 0.15s;
        }

        tbody tr:hover {
          background: var(--table-row-hover, #f8f9fa);
        }

        tbody tr:nth-child(even) {
          background: var(--table-row-even, #fafbfc);
        }

        .align-right {
          text-align: right;
        }

        a {
          color: var(--color-link, #0066cc);
          text-decoration: none;
        }

        a:hover {
          text-decoration: underline;
        }

        tfoot td {
          padding: 0.75rem 1rem;
          background: var(--table-footer-bg, #f8f9fa);
          font-size: 0.875rem;
          color: var(--color-text-secondary, #666);
        }

        .summary {
          font-weight: 500;
        }

        /* Responsive */
        @media (max-width: 768px) {
          table {
            font-size: 0.875rem;
          }

          th, td {
            padding: 0.5rem;
          }

          .sort-indicator {
            display: block;
            font-size: 0.75em;
          }
        }

        /* Accessibility - Focus styles */
        th.sortable:focus {
          outline: 2px solid var(--color-focus, #0066cc);
          outline-offset: -2px;
        }

        /* Print styles */
        @media print {
          .table-container {
            max-width: 100%;
          }

          table {
            box-shadow: none;
            border: 1px solid #ddd;
          }
        }
      `}</style>
    </div>
  );
};

export default BasicSortableTable;