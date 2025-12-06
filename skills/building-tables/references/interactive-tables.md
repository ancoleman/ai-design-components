# Interactive Table Patterns

Row selection, inline editing, expandable rows, and action buttons.


## Table of Contents

- [Row Selection](#row-selection)
  - [Single Selection](#single-selection)
  - [Multi-Selection](#multi-selection)
- [Expandable Rows](#expandable-rows)
- [Inline Editing](#inline-editing)
- [Action Buttons](#action-buttons)
- [Bulk Actions](#bulk-actions)
- [Best Practices](#best-practices)
- [Resources](#resources)

## Row Selection

### Single Selection

```tsx
function SelectableTable({ data }: { data: User[] }) {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  return (
    <table>
      <tbody>
        {data.map((row) => (
          <tr
            key={row.id}
            onClick={() => setSelectedId(row.id)}
            className={selectedId === row.id ? 'bg-blue-50' : ''}
            style={{ cursor: 'pointer' }}
          >
            <td>{row.name}</td>
            <td>{row.email}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Multi-Selection

```tsx
function MultiSelectTable({ data }: { data: User[] }) {
  const [selected, setSelected] = useState<Set<number>>(new Set());

  const toggleRow = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
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
          <th>
            <input
              type="checkbox"
              checked={selected.size === data.length}
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
                onChange={() => toggleRow(row.id)}
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

## Expandable Rows

```tsx
function ExpandableTable({ data }: { data: Order[] }) {
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const toggleRow = (id: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <table>
      <tbody>
        {data.map((order) => (
          <React.Fragment key={order.id}>
            <tr onClick={() => toggleRow(order.id)} style={{ cursor: 'pointer' }}>
              <td>{expanded.has(order.id) ? '▼' : '▶'}</td>
              <td>{order.id}</td>
              <td>{order.customer}</td>
              <td>${order.total}</td>
            </tr>

            {expanded.has(order.id) && (
              <tr>
                <td colSpan={4} className="bg-gray-50 p-4">
                  <h4>Order Items:</h4>
                  <ul>
                    {order.items.map((item) => (
                      <li key={item.id}>{item.name} - ${item.price}</li>
                    ))}
                  </ul>
                </td>
              </tr>
            )}
          </React.Fragment>
        ))}
      </tbody>
    </table>
  );
}
```

## Inline Editing

```tsx
function EditableCell({ value, onSave }: Props) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);

  const handleSave = () => {
    onSave(editValue);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <input
        value={editValue}
        onChange={(e) => setEditValue(e.target.value)}
        onBlur={handleSave}
        onKeyDown={(e) => {
          if (e.key === 'Enter') handleSave();
          if (e.key === 'Escape') setIsEditing(false);
        }}
        autoFocus
      />
    );
  }

  return (
    <div onClick={() => setIsEditing(true)} style={{ cursor: 'pointer' }}>
      {value}
    </div>
  );
}
```

## Action Buttons

```tsx
function ActionCell({ rowId }: { rowId: number }) {
  return (
    <div className="flex gap-2">
      <button
        onClick={(e) => {
          e.stopPropagation();  // Don't trigger row selection
          handleEdit(rowId);
        }}
        className="px-3 py-1 bg-blue-500 text-white rounded"
      >
        Edit
      </button>
      <button
        onClick={(e) => {
          e.stopPropagation();
          handleDelete(rowId);
        }}
        className="px-3 py-1 bg-red-500 text-white rounded"
      >
        Delete
      </button>
    </div>
  );
}
```

## Bulk Actions

```tsx
function TableWithBulkActions({ data }: { data: User[] }) {
  const [selected, setSelected] = useState<Set<number>>(new Set());

  const handleBulkDelete = async () => {
    if (!confirm(`Delete ${selected.size} users?`)) return;

    await Promise.all(
      Array.from(selected).map((id) => deleteUser(id))
    );

    setSelected(new Set());
  };

  return (
    <>
      {selected.size > 0 && (
        <div className="p-4 bg-blue-50 flex justify-between">
          <span>{selected.size} selected</span>
          <div className="flex gap-2">
            <button onClick={handleBulkDelete}>Delete</button>
            <button onClick={() => handleBulkExport(selected)}>Export</button>
            <button onClick={() => setSelected(new Set())}>Clear</button>
          </div>
        </div>
      )}

      <Table data={data} selected={selected} onSelect={setSelected} />
    </>
  );
}
```

## Best Practices

1. **Keyboard support** - Enter to select, Space to expand, Arrow keys to navigate
2. **Visual feedback** - Highlight selected/hovered rows
3. **Bulk actions** - Operate on multiple rows
4. **Inline editing** - Edit cells without modal
5. **Expandable details** - Collapse/expand additional info
6. **Action confirmation** - Confirm destructive actions
7. **Optimistic updates** - Update UI before server confirms
8. **Error handling** - Rollback on failure

## Resources

- TanStack Table: https://tanstack.com/table/
- AG Grid: https://www.ag-grid.com/
