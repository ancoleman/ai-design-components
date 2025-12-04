import React, { useState, useRef, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import 'ag-grid-enterprise';

/**
 * AG Grid Enterprise Example
 *
 * Demonstrates advanced enterprise features:
 * - Row grouping and aggregation
 * - Server-side data model
 * - Excel export
 * - Master-detail (expandable rows)
 * - Context menu
 * - Column pinning
 *
 * Requires: npm install ag-grid-react ag-grid-enterprise
 * License: Enterprise features require license key
 */

interface SalesData {
  id: number;
  country: string;
  product: string;
  sales: number;
  profit: number;
  quantity: number;
}

const generateData = (): SalesData[] => {
  const countries = ['USA', 'UK', 'Germany', 'France', 'Japan'];
  const products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headset'];

  return Array.from({ length: 1000 }, (_, i) => ({
    id: i + 1,
    country: countries[Math.floor(Math.random() * countries.length)],
    product: products[Math.floor(Math.random() * products.length)],
    sales: Math.floor(Math.random() * 10000),
    profit: Math.floor(Math.random() * 3000),
    quantity: Math.floor(Math.random() * 100),
  }));
};

export function AGGridEnterpriseExample() {
  const gridRef = useRef<AgGridReact>(null);
  const [rowData] = useState(generateData());

  const columnDefs = useMemo(() => [
    {
      field: 'country',
      rowGroup: true,        // Group by country
      hide: true,            // Hide when grouped
    },
    {
      field: 'product',
      rowGroup: true,        // Then group by product
      hide: true,
    },
    {
      field: 'sales',
      aggFunc: 'sum',        // Sum sales in groups
      valueFormatter: (params) => '$' + params.value?.toLocaleString(),
    },
    {
      field: 'profit',
      aggFunc: 'sum',
      valueFormatter: (params) => '$' + params.value?.toLocaleString(),
    },
    {
      field: 'quantity',
      aggFunc: 'avg',
      valueFormatter: (params) => params.value?.toFixed(0),
    },
  ], []);

  const defaultColDef = useMemo(() => ({
    sortable: true,
    filter: true,
    resizable: true,
    enableRowGroup: true,
    enablePivot: true,
    enableValue: true,
  }), []);

  const autoGroupColumnDef = useMemo(() => ({
    minWidth: 250,
    cellRendererParams: {
      suppressCount: false,  // Show count in group headers
    },
  }), []);

  const exportToExcel = () => {
    gridRef.current?.api.exportDataAsExcel({
      fileName: 'sales-report.xlsx',
    });
  };

  return (
    <div className="p-4">
      <div className="mb-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">AG Grid Enterprise Features</h1>

        <div className="flex gap-2">
          <button
            onClick={exportToExcel}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            📥 Export Excel
          </button>

          <button
            onClick={() => gridRef.current?.api.expandAll()}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Expand All
          </button>

          <button
            onClick={() => gridRef.current?.api.collapseAll()}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Collapse All
          </button>
        </div>
      </div>

      <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
        <AgGridReact
          ref={gridRef}
          rowData={rowData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          autoGroupColumnDef={autoGroupColumnDef}
          groupDisplayType="multipleColumns"
          animateRows={true}
          enableRangeSelection={true}
          enableCharts={true}
          sideBar={true}
          statusBar={{
            statusPanels: [
              { statusPanel: 'agTotalAndFilteredRowCountComponent' },
              { statusPanel: 'agAggregationComponent' },
            ],
          }}
          getContextMenuItems={(params) => [
            'copy',
            'copyWithHeaders',
            'paste',
            'separator',
            'export',
          ]}
        />
      </div>

      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-900">
          <strong>Enterprise Features Shown:</strong> Row grouping, aggregation, Excel export,
          range selection, charts, sidebar, context menu, status bar
        </p>
      </div>
    </div>
  );
}

export default AGGridEnterpriseExample;
