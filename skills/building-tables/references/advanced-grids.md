# Advanced Data Grid Features

Enterprise features: virtual scrolling, cell editing, aggregation, pivoting, and Excel export.


## Table of Contents

- [Virtual Scrolling (Large Datasets)](#virtual-scrolling-large-datasets)
- [Cell Editing (AG Grid)](#cell-editing-ag-grid)
- [Aggregation (Group By)](#aggregation-group-by)
- [Pivot Tables](#pivot-tables)
- [Column Pinning](#column-pinning)
- [Column Resizing](#column-resizing)
- [Excel Export](#excel-export)
- [Context Menu](#context-menu)
- [Resources](#resources)

## Virtual Scrolling (Large Datasets)

**Why:** Render only visible rows for 100K+ row performance.

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualTable({ data }: { data: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // Row height
    overscan: 10,            // Render extra rows above/below
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <TableRow data={data[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Cell Editing (AG Grid)

```tsx
import { AgGridReact } from 'ag-grid-react';

function EditableGrid() {
  const [columnDefs] = useState([
    { field: 'name', editable: true },
    { field: 'email', editable: true },
    {
      field: 'status',
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: { values: ['active', 'inactive'] },
    },
  ]);

  const onCellValueChanged = (params) => {
    console.log('Cell changed:', params.data);
    // Update database
    updateUser(params.data.id, params.data);
  };

  return (
    <AgGridReact
      columnDefs={columnDefs}
      rowData={data}
      onCellValueChanged={onCellValueChanged}
      singleClickEdit={true}
    />
  );
}
```

## Aggregation (Group By)

```tsx
// AG Grid with grouping
const columnDefs = [
  { field: 'category', rowGroup: true },  // Group by category
  { field: 'product' },
  { field: 'sales', aggFunc: 'sum' },     // Sum sales
  { field: 'units', aggFunc: 'avg' },     // Average units
];

<AgGridReact
  columnDefs={columnDefs}
  rowData={data}
  groupDisplayType="multipleColumns"
  autoGroupColumnDef={{ minWidth: 200 }}
/>
```

## Pivot Tables

```tsx
const columnDefs = [
  { field: 'country', rowGroup: true },
  { field: 'year', pivot: true },
  { field: 'revenue', aggFunc: 'sum' },
];

// Produces:
//           2023    2024    2025
// USA       $100K   $150K   $200K
// UK        $80K    $90K    $110K
```

## Column Pinning

```tsx
const columnDefs = [
  { field: 'name', pinned: 'left', width: 200 },  // Always visible
  { field: 'email' },
  { field: 'phone' },
  { field: 'address' },
  { field: 'actions', pinned: 'right' },          // Always visible
];
```

## Column Resizing

```tsx
import { useReactTable, getCoreRowModel } from '@tanstack/react-table';

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  columnResizeMode: 'onChange',
  enableColumnResizing: true,
});

// Render resizable header
<th
  style={{ width: header.getSize() }}
  onMouseDown={header.getResizeHandler()}
>
  {header.column.columnDef.header}
  <div className="resizer" />
</th>
```

## Excel Export

```tsx
import { utils, writeFile } from 'xlsx';

function exportToExcel(data: any[], filename: string) {
  const worksheet = utils.json_to_sheet(data);
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, 'Data');

  writeFile(workbook, filename);
}

<button onClick={() => exportToExcel(tableData, 'export.xlsx')}>
  Export to Excel
</button>
```

## Context Menu

```tsx
function TableWithContextMenu({ data }: Props) {
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; rowId: number } | null>(null);

  const handleContextMenu = (e: React.MouseEvent, rowId: number) => {
    e.preventDefault();
    setContextMenu({ x: e.clientX, y: e.clientY, rowId });
  };

  return (
    <>
      <table>
        {data.map((row) => (
          <tr key={row.id} onContextMenu={(e) => handleContextMenu(e, row.id)}>
            <td>{row.name}</td>
          </tr>
        ))}
      </table>

      {contextMenu && (
        <div
          style={{
            position: 'fixed',
            left: contextMenu.x,
            top: contextMenu.y,
            backgroundColor: 'white',
            border: '1px solid #ccc',
            borderRadius: '4px',
            padding: '8px',
            zIndex: 1000,
          }}
        >
          <button onClick={() => handleEdit(contextMenu.rowId)}>Edit</button>
          <button onClick={() => handleDelete(contextMenu.rowId)}>Delete</button>
        </div>
      )}

      {contextMenu && (
        <div
          onClick={() => setContextMenu(null)}
          style={{ position: 'fixed', inset: 0 }}
        />
      )}
    </>
  );
}
```

## Resources

- TanStack Table: https://tanstack.com/table/
- AG Grid Enterprise: https://www.ag-grid.com/javascript-data-grid/
