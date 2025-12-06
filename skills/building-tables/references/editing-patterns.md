# Table Editing Patterns

Inline editing, validation, optimistic updates, and bulk editing for data grids.


## Table of Contents

- [Inline Cell Editing](#inline-cell-editing)
- [Select Dropdown Editor](#select-dropdown-editor)
- [Date Picker Editor](#date-picker-editor)
- [Optimistic Updates](#optimistic-updates)
- [Validation](#validation)
- [Bulk Editing](#bulk-editing)
- [Row Reordering](#row-reordering)
- [Copy/Paste (Excel-like)](#copypaste-excel-like)
- [Formula Support](#formula-support)
- [Conditional Formatting](#conditional-formatting)
- [Resources](#resources)

## Inline Cell Editing

```tsx
function EditableCell({ value, rowId, columnId, onUpdate }: Props) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);
  const [error, setError] = useState('');

  const handleSave = async () => {
    // Validate
    if (!editValue.trim()) {
      setError('Value required');
      return;
    }

    try {
      await onUpdate(rowId, columnId, editValue);
      setIsEditing(false);
      setError('');
    } catch (err) {
      setError(err.message);
    }
  };

  if (isEditing) {
    return (
      <div>
        <input
          value={editValue}
          onChange={(e) => setEditValue(e.target.value)}
          onBlur={handleSave}
          onKeyDown={(e) => {
            if (e.key === 'Enter') handleSave();
            if (e.key === 'Escape') {
              setEditValue(value);
              setIsEditing(false);
            }
          }}
          autoFocus
        />
        {error && <span className="text-red-500 text-xs">{error}</span>}
      </div>
    );
  }

  return (
    <div
      onClick={() => setIsEditing(true)}
      className="cursor-pointer hover:bg-gray-50 p-2"
    >
      {value}
    </div>
  );
}
```

## Select Dropdown Editor

```tsx
function SelectCell({ value, options, onUpdate }: Props) {
  return (
    <select
      value={value}
      onChange={(e) => onUpdate(e.target.value)}
      className="w-full p-2"
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
}
```

## Date Picker Editor

```tsx
function DateCell({ value, onUpdate }: Props) {
  return (
    <input
      type="date"
      value={value}
      onChange={(e) => onUpdate(e.target.value)}
      className="w-full p-2"
    />
  );
}
```

## Optimistic Updates

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function EditableTable({ data }: { data: User[] }) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: ({ id, field, value }) =>
      fetch(`/api/users/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ [field]: value }),
      }),

    onMutate: async (variables) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['users'] });

      // Snapshot previous value
      const previous = queryClient.getQueryData(['users']);

      // Optimistically update
      queryClient.setQueryData(['users'], (old: User[]) =>
        old.map((user) =>
          user.id === variables.id
            ? { ...user, [variables.field]: variables.value }
            : user
        )
      );

      return { previous };
    },

    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(['users'], context?.previous);
    },

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  return <Table onCellUpdate={mutation.mutate} />;
}
```

## Validation

```tsx
const validators = {
  email: (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
  age: (value: number) => value >= 0 && value <= 120,
  required: (value: any) => value != null && value !== '',
};

function validateCell(columnId: string, value: any): string | null {
  if (validators.required(value) === false) {
    return 'This field is required';
  }

  if (columnId === 'email' && !validators.email(value)) {
    return 'Invalid email format';
  }

  return null;
}
```

## Bulk Editing

```tsx
function BulkEditTable({ data, selected }: Props) {
  const [bulkEditField, setBulkEditField] = useState('');
  const [bulkEditValue, setBulkEditValue] = useState('');

  const applyBulkEdit = async () => {
    const updates = Array.from(selected).map((id) => ({
      id,
      [bulkEditField]: bulkEditValue,
    }));

    await Promise.all(updates.map((update) => updateUser(update)));
  };

  if (selected.size === 0) return null;

  return (
    <div className="bulk-edit-panel">
      <span>{selected.size} rows selected</span>

      <select onChange={(e) => setBulkEditField(e.target.value)}>
        <option value="">Select field...</option>
        <option value="status">Status</option>
        <option value="category">Category</option>
      </select>

      <input
        value={bulkEditValue}
        onChange={(e) => setBulkEditValue(e.target.value)}
        placeholder="New value"
      />

      <button onClick={applyBulkEdit}>Apply to Selected</button>
    </div>
  );
}
```

## Row Reordering

```tsx
import { DndContext, closestCenter } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';

function SortableRow({ id, children }: Props) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <tr ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {children}
    </tr>
  );
}

function ReorderableTable({ data, onReorder }: Props) {
  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (active.id !== over.id) {
      onReorder(active.id, over.id);
    }
  };

  return (
    <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={data.map(d => d.id)} strategy={verticalListSortingStrategy}>
        <table>
          <tbody>
            {data.map((row) => (
              <SortableRow key={row.id} id={row.id}>
                <td>⋮⋮</td>
                <td>{row.name}</td>
              </SortableRow>
            ))}
          </tbody>
        </table>
      </SortableContext>
    </DndContext>
  );
}
```

## Copy/Paste (Excel-like)

```tsx
function CopyPasteTable() {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.metaKey && e.key === 'c') {
      // Copy selected cells
      const text = getSelectedCells().map(c => c.value).join('\n');
      navigator.clipboard.writeText(text);
    }

    if (e.metaKey && e.key === 'v') {
      // Paste into cells
      navigator.clipboard.readText().then((text) => {
        pasteIntoCells(text);
      });
    }
  };

  return <table onKeyDown={handleKeyDown} />;
}
```

## Formula Support

```tsx
// Cell with formula
{
  value: '=SUM(A1:A10)',
  computed: 450,  // Evaluated result
  type: 'formula',
}

function evaluateFormula(formula: string, data: any[]): number {
  if (formula.startsWith('=SUM')) {
    const range = formula.match(/\((.+)\)/)[1];
    return data.reduce((sum, row) => sum + row.value, 0);
  }
  // ... other formulas
}
```

## Conditional Formatting

```tsx
function ConditionalCell({ value, rules }: Props) {
  const style = rules.find((rule) => rule.condition(value))?.style;

  return (
    <td style={style}>
      {value}
    </td>
  );
}

const rules = [
  {
    condition: (val) => val > 1000,
    style: { backgroundColor: '#dcfce7', color: '#166534' },  // Green
  },
  {
    condition: (val) => val < 0,
    style: { backgroundColor: '#fee2e2', color: '#991b1b' },  // Red
  },
];
```

## Resources

- AG Grid Enterprise: https://www.ag-grid.com/
- Handsontable: https://handsontable.com/
- TanStack Virtual: https://tanstack.com/virtual/
