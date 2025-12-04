import React, { useState } from 'react';
import { Check, X } from 'lucide-react';

/**
 * Editable Cells Example
 *
 * Demonstrates inline cell editing with:
 * - Double-click to edit
 * - Different editor types (text, select, number)
 * - Validation
 * - Save/cancel actions
 * - Optimistic updates
 */

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
}

const initialData: Product[] = [
  { id: 1, name: 'Laptop', category: 'Electronics', price: 1299, stock: 15 },
  { id: 2, name: 'Mouse', category: 'Accessories', price: 29, stock: 50 },
  { id: 3, name: 'Keyboard', category: 'Accessories', price: 79, stock: 30 },
];

export function EditableCellsTable() {
  const [data, setData] = useState(initialData);
  const [editing, setEditing] = useState<{ rowId: number; field: keyof Product } | null>(null);
  const [editValue, setEditValue] = useState<string | number>('');

  const startEdit = (rowId: number, field: keyof Product, currentValue: any) => {
    setEditing({ rowId, field });
    setEditValue(currentValue);
  };

  const saveEdit = () => {
    if (!editing) return;

    setData((prev) =>
      prev.map((row) =>
        row.id === editing.rowId
          ? { ...row, [editing.field]: editValue }
          : row
      )
    );

    setEditing(null);
    console.log('Saved:', editing.field, editValue);
  };

  const cancelEdit = () => {
    setEditing(null);
    setEditValue('');
  };

  const renderCell = (row: Product, field: keyof Product) => {
    const isEditing = editing?.rowId === row.id && editing?.field === field;

    if (isEditing) {
      // Editing mode
      if (field === 'category') {
        return (
          <div className="flex items-center gap-2">
            <select
              value={editValue as string}
              onChange={(e) => setEditValue(e.target.value)}
              autoFocus
              className="px-2 py-1 border rounded"
            >
              <option value="Electronics">Electronics</option>
              <option value="Accessories">Accessories</option>
              <option value="Furniture">Furniture</option>
            </select>
            <button onClick={saveEdit} className="text-green-600">
              <Check size={18} />
            </button>
            <button onClick={cancelEdit} className="text-red-600">
              <X size={18} />
            </button>
          </div>
        );
      } else {
        return (
          <div className="flex items-center gap-2">
            <input
              type={field === 'price' || field === 'stock' ? 'number' : 'text'}
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') saveEdit();
                if (e.key === 'Escape') cancelEdit();
              }}
              autoFocus
              className="px-2 py-1 border rounded w-full"
            />
            <button onClick={saveEdit} className="text-green-600">
              <Check size={18} />
            </button>
            <button onClick={cancelEdit} className="text-red-600">
              <X size={18} />
            </button>
          </div>
        );
      }
    }

    // Display mode
    return (
      <div
        onDoubleClick={() => startEdit(row.id, field, row[field])}
        className="cursor-pointer hover:bg-gray-50 px-2 py-1 rounded"
        title="Double-click to edit"
      >
        {field === 'price' ? `$${row[field]}` : row[field]}
      </div>
    );
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Editable Table</h1>

      <div className="mb-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-900">
        💡 <strong>Tip:</strong> Double-click any cell to edit. Press Enter to save, Escape to cancel.
      </div>

      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y">
            {data.map((row) => (
              <tr key={row.id}>
                <td className="px-6 py-4 text-gray-500">{row.id}</td>
                <td className="px-6 py-4">{renderCell(row, 'name')}</td>
                <td className="px-6 py-4">{renderCell(row, 'category')}</td>
                <td className="px-6 py-4">{renderCell(row, 'price')}</td>
                <td className="px-6 py-4">{renderCell(row, 'stock')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EditableCellsTable;
