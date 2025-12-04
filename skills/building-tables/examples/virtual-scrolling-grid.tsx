import React, { useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

/**
 * Virtual Scrolling Table Example
 *
 * Efficiently renders large datasets (10K+ rows) by only rendering visible rows.
 * Uses @tanstack/react-virtual for performance.
 *
 * Install: npm install @tanstack/react-virtual
 */

interface DataRow {
  id: number;
  name: string;
  value: number;
  category: string;
}

// Generate large dataset
const generateData = (count: number): DataRow[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    name: `Item ${i + 1}`,
    value: Math.floor(Math.random() * 1000),
    category: ['A', 'B', 'C', 'D'][Math.floor(Math.random() * 4)],
  }));
};

export function VirtualScrollingGrid() {
  const parentRef = useRef<HTMLDivElement>(null);
  const data = useRef(generateData(10000)).current;  // 10,000 rows

  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // Estimated row height
    overscan: 20,            // Render 20 extra rows above/below viewport
  });

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">
        Virtual Scrolling Grid ({data.length.toLocaleString()} rows)
      </h1>

      <div
        ref={parentRef}
        className="border rounded-lg"
        style={{
          height: '600px',
          overflow: 'auto',
        }}
      >
        {/* Header (sticky) */}
        <div
          style={{
            position: 'sticky',
            top: 0,
            zIndex: 10,
            backgroundColor: '#f9fafb',
            borderBottom: '1px solid #e5e7eb',
            display: 'grid',
            gridTemplateColumns: '80px 1fr 120px 120px',
            padding: '12px 16px',
            fontWeight: 600,
            fontSize: '14px',
            color: '#6b7280',
          }}
        >
          <div>ID</div>
          <div>Name</div>
          <div>Value</div>
          <div>Category</div>
        </div>

        {/* Virtual rows */}
        <div
          style={{
            height: `${virtualizer.getTotalSize()}px`,
            width: '100%',
            position: 'relative',
          }}
        >
          {virtualizer.getVirtualItems().map((virtualRow) => {
            const row = data[virtualRow.index];

            return (
              <div
                key={virtualRow.key}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: `${virtualRow.size}px`,
                  transform: `translateY(${virtualRow.start}px)`,
                  display: 'grid',
                  gridTemplateColumns: '80px 1fr 120px 120px',
                  padding: '12px 16px',
                  borderBottom: '1px solid #f3f4f6',
                  backgroundColor: virtualRow.index % 2 === 0 ? '#fff' : '#f9fafb',
                }}
              >
                <div className="text-gray-500">{row.id}</div>
                <div className="font-medium">{row.name}</div>
                <div className="text-blue-600">${row.value}</div>
                <div>
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                    {row.category}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        Only rendering ~{virtualizer.getVirtualItems().length} rows at a time (out of {data.length.toLocaleString()})
      </div>
    </div>
  );
}

export default VirtualScrollingGrid;
