import React, { useState, useMemo } from 'react';

/**
 * Paginated Table Example
 * Demonstrates client-side pagination for medium datasets (100-1000 rows)
 */

interface DataRow {
  id: number;
  name: string;
  email: string;
  role: string;
  department: string;
  location: string;
  status: 'Active' | 'Inactive' | 'Pending';
  lastLogin: string;
}

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  pageSize: number;
  totalItems: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: number) => void;
}

const PaginationControls: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  pageSize,
  totalItems,
  onPageChange,
  onPageSizeChange
}) => {
  // Calculate page numbers to display
  const getPageNumbers = () => {
    const delta = 2;
    const range: (number | string)[] = [];

    for (let i = Math.max(2, currentPage - delta); i <= Math.min(totalPages - 1, currentPage + delta); i++) {
      range.push(i);
    }

    if (currentPage - delta > 2) {
      range.unshift('...');
    }
    range.unshift(1);

    if (currentPage + delta < totalPages - 1) {
      range.push('...');
    }
    if (totalPages > 1) {
      range.push(totalPages);
    }

    return range;
  };

  const startItem = (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalItems);

  return (
    <div className="pagination-controls">
      <div className="pagination-info">
        <span>
          Showing {startItem} to {endItem} of {totalItems} entries
        </span>
        <select
          value={pageSize}
          onChange={(e) => onPageSizeChange(Number(e.target.value))}
          aria-label="Items per page"
        >
          <option value={10}>10 per page</option>
          <option value={25}>25 per page</option>
          <option value={50}>50 per page</option>
          <option value={100}>100 per page</option>
        </select>
      </div>

      <nav aria-label="Pagination Navigation">
        <ul className="pagination">
          <li className={currentPage === 1 ? 'disabled' : ''}>
            <button
              onClick={() => onPageChange(1)}
              disabled={currentPage === 1}
              aria-label="Go to first page"
            >
              First
            </button>
          </li>

          <li className={currentPage === 1 ? 'disabled' : ''}>
            <button
              onClick={() => onPageChange(currentPage - 1)}
              disabled={currentPage === 1}
              aria-label="Go to previous page"
            >
              Previous
            </button>
          </li>

          {getPageNumbers().map((number, index) => (
            <li
              key={index}
              className={number === currentPage ? 'active' : number === '...' ? 'ellipsis' : ''}
            >
              {number === '...' ? (
                <span>...</span>
              ) : (
                <button
                  onClick={() => onPageChange(number as number)}
                  aria-label={`Go to page ${number}`}
                  aria-current={number === currentPage ? 'page' : undefined}
                >
                  {number}
                </button>
              )}
            </li>
          ))}

          <li className={currentPage === totalPages ? 'disabled' : ''}>
            <button
              onClick={() => onPageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              aria-label="Go to next page"
            >
              Next
            </button>
          </li>

          <li className={currentPage === totalPages ? 'disabled' : ''}>
            <button
              onClick={() => onPageChange(totalPages)}
              disabled={currentPage === totalPages}
              aria-label="Go to last page"
            >
              Last
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

const PaginatedTable: React.FC = () => {
  // Generate sample data (simulating larger dataset)
  const generateData = (): DataRow[] => {
    const departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'];
    const roles = ['Manager', 'Senior', 'Junior', 'Lead', 'Analyst', 'Specialist'];
    const locations = ['New York', 'San Francisco', 'London', 'Tokyo', 'Berlin', 'Sydney'];
    const statuses: ('Active' | 'Inactive' | 'Pending')[] = ['Active', 'Inactive', 'Pending'];

    return Array.from({ length: 250 }, (_, i) => ({
      id: i + 1,
      name: `Employee ${i + 1}`,
      email: `employee${i + 1}@example.com`,
      role: roles[Math.floor(Math.random() * roles.length)],
      department: departments[Math.floor(Math.random() * departments.length)],
      location: locations[Math.floor(Math.random() * locations.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      lastLogin: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
    }));
  };

  const allData = useMemo(() => generateData(), []);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [searchTerm, setSearchTerm] = useState('');

  // Filter data based on search
  const filteredData = useMemo(() => {
    if (!searchTerm) return allData;

    return allData.filter(row =>
      Object.values(row).some(value =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [allData, searchTerm]);

  // Calculate pagination
  const totalPages = Math.ceil(filteredData.length / pageSize);

  // Get current page data
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return filteredData.slice(startIndex, endIndex);
  }, [filteredData, currentPage, pageSize]);

  // Handle page size change
  const handlePageSizeChange = (newSize: number) => {
    setPageSize(newSize);
    setCurrentPage(1); // Reset to first page
  };

  // Handle search
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1); // Reset to first page on search
  };

  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Get status badge class
  const getStatusClass = (status: string) => {
    switch (status) {
      case 'Active': return 'badge-success';
      case 'Inactive': return 'badge-danger';
      case 'Pending': return 'badge-warning';
      default: return 'badge-default';
    }
  };

  return (
    <div className="table-container">
      <div className="table-header">
        <h2>User Management</h2>
        <div className="search-box">
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={handleSearch}
            aria-label="Search table"
          />
          {searchTerm && (
            <button
              onClick={() => {
                setSearchTerm('');
                setCurrentPage(1);
              }}
              className="clear-search"
              aria-label="Clear search"
            >
              ×
            </button>
          )}
        </div>
      </div>

      <table role="table">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
            <th scope="col">Role</th>
            <th scope="col">Department</th>
            <th scope="col">Location</th>
            <th scope="col">Status</th>
            <th scope="col">Last Login</th>
          </tr>
        </thead>

        <tbody>
          {paginatedData.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.name}</td>
              <td>
                <a href={`mailto:${row.email}`}>{row.email}</a>
              </td>
              <td>{row.role}</td>
              <td>{row.department}</td>
              <td>{row.location}</td>
              <td>
                <span className={`badge ${getStatusClass(row.status)}`}>
                  {row.status}
                </span>
              </td>
              <td>{formatDate(row.lastLogin)}</td>
            </tr>
          ))}

          {paginatedData.length === 0 && (
            <tr>
              <td colSpan={8} className="no-data">
                {searchTerm ? 'No results found' : 'No data available'}
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <PaginationControls
        currentPage={currentPage}
        totalPages={totalPages}
        pageSize={pageSize}
        totalItems={filteredData.length}
        onPageChange={setCurrentPage}
        onPageSizeChange={handlePageSizeChange}
      />

      <style jsx>{`
        .table-container {
          max-width: 1400px;
          margin: 2rem auto;
          padding: 0 1rem;
          font-family: system-ui, -apple-system, sans-serif;
        }

        .table-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        h2 {
          margin: 0;
          color: var(--color-text-primary, #1a1a1a);
        }

        .search-box {
          position: relative;
          width: 300px;
        }

        .search-box input {
          width: 100%;
          padding: 0.5rem 2rem 0.5rem 1rem;
          border: 1px solid var(--border-color, #ddd);
          border-radius: 4px;
          font-size: 0.875rem;
        }

        .clear-search {
          position: absolute;
          right: 0.5rem;
          top: 50%;
          transform: translateY(-50%);
          background: none;
          border: none;
          font-size: 1.5rem;
          cursor: pointer;
          padding: 0 0.25rem;
          color: var(--color-text-secondary, #666);
        }

        table {
          width: 100%;
          border-collapse: collapse;
          background: white;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          border-radius: 8px;
          overflow: hidden;
        }

        th {
          background: var(--table-header-bg, #f8f9fa);
          padding: 0.75rem 1rem;
          text-align: left;
          font-weight: 600;
          color: var(--table-header-text, #495057);
          border-bottom: 2px solid var(--table-border, #dee2e6);
        }

        td {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--table-border, #dee2e6);
        }

        tbody tr:hover {
          background: var(--table-row-hover, #f8f9fa);
        }

        .no-data {
          text-align: center;
          color: var(--color-text-secondary, #666);
          padding: 2rem;
        }

        .badge {
          display: inline-block;
          padding: 0.25rem 0.5rem;
          font-size: 0.75rem;
          font-weight: 600;
          border-radius: 4px;
          text-transform: uppercase;
        }

        .badge-success {
          background: #d4edda;
          color: #155724;
        }

        .badge-danger {
          background: #f8d7da;
          color: #721c24;
        }

        .badge-warning {
          background: #fff3cd;
          color: #856404;
        }

        /* Pagination styles */
        .pagination-controls {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 1rem;
          padding: 1rem;
          background: var(--table-footer-bg, #f8f9fa);
          border-radius: 0 0 8px 8px;
        }

        .pagination-info {
          display: flex;
          align-items: center;
          gap: 1rem;
          font-size: 0.875rem;
          color: var(--color-text-secondary, #666);
        }

        .pagination-info select {
          padding: 0.25rem 0.5rem;
          border: 1px solid var(--border-color, #ddd);
          border-radius: 4px;
        }

        .pagination {
          display: flex;
          list-style: none;
          margin: 0;
          padding: 0;
          gap: 0.25rem;
        }

        .pagination li button {
          padding: 0.5rem 0.75rem;
          background: white;
          border: 1px solid var(--border-color, #ddd);
          color: var(--color-text-primary, #1a1a1a);
          cursor: pointer;
          transition: all 0.2s;
          font-size: 0.875rem;
        }

        .pagination li button:hover:not(:disabled) {
          background: var(--color-primary-light, #e3f2fd);
          border-color: var(--color-primary, #2196f3);
        }

        .pagination li.active button {
          background: var(--color-primary, #2196f3);
          color: white;
          border-color: var(--color-primary, #2196f3);
        }

        .pagination li.disabled button {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .pagination li.ellipsis span {
          padding: 0.5rem 0.75rem;
          color: var(--color-text-secondary, #666);
        }

        /* Responsive */
        @media (max-width: 768px) {
          .table-header {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
          }

          .search-box {
            width: 100%;
          }

          .pagination-controls {
            flex-direction: column;
            gap: 1rem;
          }

          table {
            font-size: 0.875rem;
          }

          th, td {
            padding: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default PaginatedTable;