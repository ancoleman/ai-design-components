# Table Selection Patterns

Row selection, cell selection, and range selection patterns for data tables.

## Single Row Selection

```tsx
function SingleSelectTable({ data }: { data: User[] }) {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  return (
    <table>
      <tbody>
        {data.map((row) => (
          <tr
            key={row.id}
            onClick={() => setSelectedId(row.id)}
            className={selectedId === row.id ? 'bg-blue-50 border-2 border-blue-500' : ''}
            style={{ cursor: 'pointer' }}
          >
            <td>{row.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Multi-Row Selection (Checkbox)

```tsx
function MultiSelectTable({ data }: { data: User[] }) {
  const [selected, setSelected] = useState<Set<number>>(new Set());

  const toggleRow = (id: number, shiftKey: boolean = false) => {
    if (shiftKey && lastSelected !== null) {
      // Shift+click: Select range
      const start = data.findIndex((r) => r.id === lastSelected);
      const end = data.findIndex((r) => r.id === id);
      const range = data.slice(Math.min(start, end), Math.max(start, end) + 1);

      setSelected((prev) => {
        const next = new Set(prev);
        range.forEach((r) => next.add(r.id));
        return next;
      });
    } else {
      // Regular click: Toggle single
      setSelected((prev) => {
        const next = new Set(prev);
        if (next.has(id)) {
          next.delete(id);
        } else {
          next.add(id);
        }
        return next;
      });
    }

    setLastSelected(id);
  };

  const toggleAll = () => {
    if (selected.size === data.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(data.map((r) => r.id)));
    }
  };

  return (
    <table>
      <thead>
        <tr>
          <th className="w-12">
            <input
              type="checkbox"
              checked={selected.size === data.length}
              indeterminate={selected.size > 0 && selected.size < data.length}
              onChange={toggleAll}
            />
          </th>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr key={row.id}>
            <td>
              <input
                type="checkbox"
                checked={selected.has(row.id)}
                onChange={(e) => toggleRow(row.id, e.shiftKey)}
              />
            </td>
            <td>{row.name}</td>
            <td>{row.email}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Keyboard Selection

```tsx
function KeyboardSelectTable({ data }: { data: User[] }) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => Math.min(prev + 1, data.length - 1));
    }

    if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => Math.max(prev - 1, 0));
    }

    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleAction(data[selectedIndex]);
    }
  };

  return (
    <table tabIndex={0} onKeyDown={handleKeyDown}>
      <tbody>
        {data.map((row, index) => (
          <tr
            key={row.id}
            className={selectedIndex === index ? 'bg-blue-50' : ''}
          >
            <td>{row.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Cell Selection (Spreadsheet-like)

```tsx
function CellSelectTable() {
  const [selectedCell, setSelectedCell] = useState<{ row: number; col: number } | null>(null);

  return (
    <table>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {Object.values(row).map((cell, colIndex) => (
              <td
                key={colIndex}
                onClick={() => setSelectedCell({ row: rowIndex, col: colIndex })}
                className={
                  selectedCell?.row === rowIndex && selectedCell?.col === colIndex
                    ? 'ring-2 ring-blue-500'
                    : ''
                }
              >
                {cell}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Range Selection (Drag)

```tsx
function RangeSelectTable() {
  const [rangeStart, setRangeStart] = useState<Cell | null>(null);
  const [rangeEnd, setRangeEnd] = useState<Cell | null>(null);

  const handleMouseDown = (row: number, col: number) => {
    setRangeStart({ row, col });
    setRangeEnd({ row, col });
  };

  const handleMouseEnter = (row: number, col: number) => {
    if (rangeStart) {
      setRangeEnd({ row, col });
    }
  };

  const isInRange = (row: number, col: number) => {
    if (!rangeStart || !rangeEnd) return false;

    const rowMin = Math.min(rangeStart.row, rangeEnd.row);
    const rowMax = Math.max(rangeStart.row, rangeEnd.row);
    const colMin = Math.min(rangeStart.col, rangeEnd.col);
    const colMax = Math.max(rangeStart.col, rangeEnd.col);

    return row >= rowMin && row <= rowMax && col >= colMin && col <= colMax;
  };

  return (
    <table onMouseUp={() => setRangeStart(null)}>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {Object.values(row).map((cell, colIndex) => (
              <td
                key={colIndex}
                onMouseDown={() => handleMouseDown(rowIndex, colIndex)}
                onMouseEnter={() => handleMouseEnter(rowIndex, colIndex)}
                className={isInRange(rowIndex, colIndex) ? 'bg-blue-100' : ''}
              >
                {cell}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Select All Variants

### Select All (Current Page)

```tsx
const toggleAllOnPage = () => {
  const pageIds = currentPageData.map((r) => r.id);
  setSelected((prev) => {
    const next = new Set(prev);
    const allSelected = pageIds.every((id) => next.has(id));

    if (allSelected) {
      pageIds.forEach((id) => next.delete(id));
    } else {
      pageIds.forEach((id) => next.add(id));
    }

    return next;
  });
};
```

### Select All (All Pages)

```tsx
const selectAllPages = async () => {
  const allIds = await fetchAllIds();  // Server-side query
  setSelected(new Set(allIds));
};

{selected.size > 0 && selected.size === currentPageData.length && (
  <div className="p-2 bg-blue-50">
    {selected.size} rows on this page selected.
    <button onClick={selectAllPages}>Select all {totalCount} rows</button>
  </div>
)}
```

## Indeterminate Checkbox

```tsx
function IndeterminateCheckbox({ checked, indeterminate, ...props }: Props) {
  const ref = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.indeterminate = indeterminate;
    }
  }, [indeterminate]);

  return <input type="checkbox" ref={ref} checked={checked} {...props} />;
}

// Usage
<IndeterminateCheckbox
  checked={selected.size === data.length}
  indeterminate={selected.size > 0 && selected.size < data.length}
  onChange={toggleAll}
/>
```

## Persist Selection

```tsx
// Save to localStorage
useEffect(() => {
  localStorage.setItem('tableSelection', JSON.stringify(Array.from(selected)));
}, [selected]);

// Restore on mount
useEffect(() => {
  const saved = localStorage.getItem('tableSelection');
  if (saved) {
    setSelected(new Set(JSON.parse(saved)));
  }
}, []);
```

## Best Practices

1. **Shift+click range select** - Select consecutive rows
2. **Cmd/Ctrl+click** - Multi-select non-consecutive
3. **Checkbox in header** - Select/deselect all
4. **Indeterminate state** - Show partial selection
5. **Visual feedback** - Highlight selected rows
6. **Keyboard support** - Arrow keys + Space/Enter
7. **Persist selection** - Save across page loads (if appropriate)
8. **Clear selection button** - Easy way to deselect all
9. **Selection count** - Show "X items selected"
10. **Bulk actions** - Enable when items selected

## Resources

- TanStack Table Selection: https://tanstack.com/table/v8/docs/guide/row-selection
- AG Grid Selection: https://www.ag-grid.com/javascript-data-grid/row-selection/
