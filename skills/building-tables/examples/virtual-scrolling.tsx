import React, { useRef, useState, useEffect, useCallback } from 'react';

/**
 * Virtual Scrolling Table Example
 * Demonstrates high-performance rendering for large datasets (10,000+ rows)
 * Only renders visible rows in the viewport for optimal performance
 */

interface DataRow {
  id: number;
  name: string;
  email: string;
  company: string;
  revenue: number;
  employees: number;
  founded: number;
  industry: string;
  status: string;
}

interface VirtualScrollProps {
  data: DataRow[];
  rowHeight: number;
  containerHeight: number;
  overscan?: number; // Number of rows to render outside viewport
}

const VirtualScrollTable: React.FC<VirtualScrollProps> = ({
  data,
  rowHeight,
  containerHeight,
  overscan = 5
}) => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [isScrolling, setIsScrolling] = useState(false);

  // Calculate visible range
  const visibleRowCount = Math.ceil(containerHeight / rowHeight);
  const startIndex = Math.max(0, Math.floor(scrollTop / rowHeight) - overscan);
  const endIndex = Math.min(
    data.length,
    Math.ceil((scrollTop + containerHeight) / rowHeight) + overscan
  );

  // Total height for scrollbar
  const totalHeight = data.length * rowHeight;

  // Get visible items
  const visibleItems = data.slice(startIndex, endIndex);

  // Handle scroll with debouncing
  const scrollTimeout = useRef<NodeJS.Timeout>();
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    const newScrollTop = e.currentTarget.scrollTop;
    setScrollTop(newScrollTop);
    setIsScrolling(true);

    // Clear existing timeout
    if (scrollTimeout.current) {
      clearTimeout(scrollTimeout.current);
    }

    // Set scrolling to false after scrolling stops
    scrollTimeout.current = setTimeout(() => {
      setIsScrolling(false);
    }, 150);
  }, []);

  // Format number
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  // Format currency
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(amount);
  };

  return (
    <div className="virtual-table-wrapper">
      <div className="table-header-fixed">
        <table>
          <thead>
            <tr>
              <th style={{ width: '80px' }}>ID</th>
              <th style={{ width: '200px' }}>Company</th>
              <th style={{ width: '250px' }}>Contact</th>
              <th style={{ width: '150px' }}>Revenue</th>
              <th style={{ width: '120px' }}>Employees</th>
              <th style={{ width: '100px' }}>Founded</th>
              <th style={{ width: '150px' }}>Industry</th>
              <th style={{ width: '100px' }}>Status</th>
            </tr>
          </thead>
        </table>
      </div>

      <div
        ref={scrollContainerRef}
        className="scroll-container"
        style={{ height: containerHeight }}
        onScroll={handleScroll}
      >
        <div
          className="scroll-height"
          style={{ height: totalHeight }}
        >
          <div
            className="visible-window"
            style={{
              transform: `translateY(${startIndex * rowHeight}px)`
            }}
          >
            <table>
              <tbody>
                {visibleItems.map((row, index) => (
                  <tr
                    key={row.id}
                    style={{ height: rowHeight }}
                    className={isScrolling ? 'scrolling' : ''}
                  >
                    <td style={{ width: '80px' }}>{row.id}</td>
                    <td style={{ width: '200px' }}>{row.company}</td>
                    <td style={{ width: '250px' }}>
                      <div className="contact-cell">
                        <div>{row.name}</div>
                        <div className="email">{row.email}</div>
                      </div>
                    </td>
                    <td style={{ width: '150px' }}>{formatCurrency(row.revenue)}</td>
                    <td style={{ width: '120px' }}>{formatNumber(row.employees)}</td>
                    <td style={{ width: '100px' }}>{row.founded}</td>
                    <td style={{ width: '150px' }}>{row.industry}</td>
                    <td style={{ width: '100px' }}>
                      <span className={`status status-${row.status.toLowerCase()}`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="table-footer">
        <div className="footer-info">
          Rendering rows {startIndex + 1} - {Math.min(endIndex, data.length)} of {formatNumber(data.length)}
        </div>
        <div className="performance-info">
          <span className="metric">
            DOM Nodes: <strong>{endIndex - startIndex}</strong>
          </span>
          <span className="metric">
            Memory: <strong>~{((endIndex - startIndex) * 0.5).toFixed(1)}KB</strong>
          </span>
          <span className="metric">
            Status: <strong className={isScrolling ? 'scrolling' : 'idle'}>
              {isScrolling ? 'Scrolling' : 'Idle'}
            </strong>
          </span>
        </div>
      </div>

      <style jsx>{`
        .virtual-table-wrapper {
          background: white;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          overflow: hidden;
        }

        .table-header-fixed {
          position: sticky;
          top: 0;
          z-index: 10;
          background: white;
          border-bottom: 2px solid var(--table-border, #dee2e6);
        }

        .scroll-container {
          overflow-y: auto;
          overflow-x: hidden;
          position: relative;
        }

        .scroll-height {
          position: relative;
          width: 100%;
        }

        .visible-window {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
        }

        table {
          width: 100%;
          border-collapse: collapse;
          table-layout: fixed;
        }

        th {
          padding: 1rem;
          text-align: left;
          font-weight: 600;
          background: var(--table-header-bg, #f8f9fa);
          color: var(--table-header-text, #495057);
          position: sticky;
          top: 0;
        }

        td {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--table-border, #e9ecef);
        }

        tr {
          background: white;
          transition: background-color 0.15s;
        }

        tr:hover {
          background: var(--table-row-hover, #f8f9fa);
        }

        tr.scrolling {
          pointer-events: none;
        }

        .contact-cell {
          line-height: 1.3;
        }

        .email {
          font-size: 0.85em;
          color: var(--color-text-secondary, #6c757d);
        }

        .status {
          display: inline-block;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
        }

        .status-active {
          background: #d4edda;
          color: #155724;
        }

        .status-pending {
          background: #fff3cd;
          color: #856404;
        }

        .status-inactive {
          background: #f8d7da;
          color: #721c24;
        }

        .table-footer {
          display: flex;
          justify-content: space-between;
          padding: 1rem;
          background: var(--table-footer-bg, #f8f9fa);
          border-top: 1px solid var(--table-border, #dee2e6);
          font-size: 0.875rem;
        }

        .footer-info {
          color: var(--color-text-secondary, #6c757d);
        }

        .performance-info {
          display: flex;
          gap: 1.5rem;
        }

        .metric {
          color: var(--color-text-secondary, #6c757d);
        }

        .metric strong {
          color: var(--color-text-primary, #212529);
          font-weight: 600;
        }

        .metric .scrolling {
          color: var(--color-warning, #ffc107);
        }

        .metric .idle {
          color: var(--color-success, #28a745);
        }

        /* Custom scrollbar */
        .scroll-container::-webkit-scrollbar {
          width: 12px;
        }

        .scroll-container::-webkit-scrollbar-track {
          background: #f1f1f1;
        }

        .scroll-container::-webkit-scrollbar-thumb {
          background: #888;
          border-radius: 6px;
        }

        .scroll-container::-webkit-scrollbar-thumb:hover {
          background: #555;
        }
      `}</style>
    </div>
  );
};

// Main component with data generation
const VirtualScrollingExample: React.FC = () => {
  const [rowCount, setRowCount] = useState(10000);
  const [data, setData] = useState<DataRow[]>([]);

  // Generate large dataset
  useEffect(() => {
    const industries = [
      'Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing',
      'Energy', 'Telecommunications', 'Transportation', 'Real Estate', 'Education'
    ];

    const statuses = ['Active', 'Pending', 'Inactive'];

    const companies = [
      'Acme Corp', 'Global Tech', 'Innovate Inc', 'Digital Solutions', 'Future Systems',
      'Smart Industries', 'Quantum Dynamics', 'Nexus Enterprises', 'Apex Innovations', 'Synergy Group'
    ];

    const firstNames = ['John', 'Jane', 'Michael', 'Sarah', 'Robert', 'Lisa', 'David', 'Emma'];
    const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'];

    const newData: DataRow[] = Array.from({ length: rowCount }, (_, i) => ({
      id: i + 1,
      name: `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`,
      email: `contact${i + 1}@company.com`,
      company: `${companies[Math.floor(Math.random() * companies.length)]} ${i + 1}`,
      revenue: Math.floor(Math.random() * 100000000) + 1000000,
      employees: Math.floor(Math.random() * 10000) + 10,
      founded: Math.floor(Math.random() * 50) + 1970,
      industry: industries[Math.floor(Math.random() * industries.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)]
    }));

    setData(newData);
  }, [rowCount]);

  return (
    <div className="container">
      <div className="header">
        <h1>Virtual Scrolling Table</h1>
        <div className="controls">
          <label>
            Row Count:
            <select
              value={rowCount}
              onChange={(e) => setRowCount(Number(e.target.value))}
            >
              <option value={1000}>1,000 rows</option>
              <option value={10000}>10,000 rows</option>
              <option value={50000}>50,000 rows</option>
              <option value={100000}>100,000 rows</option>
              <option value={500000}>500,000 rows</option>
              <option value={1000000}>1,000,000 rows</option>
            </select>
          </label>
          <div className="info">
            Only visible rows are rendered in the DOM for optimal performance
          </div>
        </div>
      </div>

      <VirtualScrollTable
        data={data}
        rowHeight={60}
        containerHeight={600}
        overscan={5}
      />

      <style jsx>{`
        .container {
          max-width: 1400px;
          margin: 2rem auto;
          padding: 0 1rem;
          font-family: system-ui, -apple-system, sans-serif;
        }

        .header {
          margin-bottom: 2rem;
        }

        h1 {
          margin-bottom: 1rem;
          color: var(--color-text-primary, #212529);
        }

        .controls {
          display: flex;
          align-items: center;
          gap: 2rem;
        }

        label {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 500;
        }

        select {
          padding: 0.5rem;
          border: 1px solid var(--border-color, #dee2e6);
          border-radius: 4px;
          font-size: 1rem;
        }

        .info {
          color: var(--color-text-secondary, #6c757d);
          font-style: italic;
        }
      `}</style>
    </div>
  );
};

export default VirtualScrollingExample;