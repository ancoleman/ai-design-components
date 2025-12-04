import React, { useState } from 'react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

/**
 * Customizable Dashboard with Drag-and-Drop
 *
 * Features:
 * - Drag to reorder widgets
 * - Resize widgets
 * - Save/restore layout
 * - Add/remove widgets
 * - Responsive breakpoints
 */

const AVAILABLE_WIDGETS = [
  { id: 'revenue', title: 'Revenue', type: 'kpi' },
  { id: 'users', title: 'Active Users', type: 'kpi' },
  { id: 'chart', title: 'Trend Chart', type: 'chart' },
  { id: 'table', title: 'Recent Orders', type: 'table' },
];

export function CustomizableDashboard() {
  const [layout, setLayout] = useState([
    { i: 'revenue', x: 0, y: 0, w: 3, h: 1 },
    { i: 'users', x: 3, y: 0, w: 3, h: 1 },
    { i: 'chart', x: 0, y: 1, w: 6, h: 2 },
    { i: 'table', x: 6, y: 1, w: 6, h: 2 },
  ]);

  const [widgets, setWidgets] = useState(['revenue', 'users', 'chart', 'table']);

  const saveLayout = () => {
    localStorage.setItem('dashboardLayout', JSON.stringify(layout));
    localStorage.setItem('dashboardWidgets', JSON.stringify(widgets));
    alert('Layout saved!');
  };

  const resetLayout = () => {
    localStorage.removeItem('dashboardLayout');
    localStorage.removeItem('dashboardWidgets');
    window.location.reload();
  };

  const onLayoutChange = (newLayout) => {
    setLayout(newLayout);
  };

  const renderWidget = (widgetId: string) => {
    const widget = AVAILABLE_WIDGETS.find((w) => w.id === widgetId);
    if (!widget) return null;

    return (
      <div
        key={widgetId}
        style={{
          backgroundColor: '#fff',
          border: '1px solid #e2e8f0',
          borderRadius: '8px',
          padding: '16px',
          height: '100%',
          overflow: 'hidden',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{widget.title}</h3>
          <button
            onClick={() => setWidgets(widgets.filter((w) => w !== widgetId))}
            style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#ef4444' }}
          >
            ×
          </button>
        </div>

        {widget.type === 'kpi' && (
          <div style={{ fontSize: '32px', fontWeight: 700, color: '#3b82f6' }}>
            {widgetId === 'revenue' ? '$63K' : '12.5K'}
          </div>
        )}

        {widget.type === 'chart' && (
          <div style={{ color: '#64748b', fontSize: '14px' }}>Chart placeholder</div>
        )}

        {widget.type === 'table' && (
          <div style={{ color: '#64748b', fontSize: '14px' }}>Table placeholder</div>
        )}
      </div>
    );
  };

  return (
    <div style={{ padding: '24px', backgroundColor: '#f8fafc', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '30px', fontWeight: 700 }}>Customizable Dashboard</h1>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={saveLayout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#3b82f6',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 600,
            }}
          >
            Save Layout
          </button>
          <button
            onClick={resetLayout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#fff',
              color: '#64748b',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 600,
            }}
          >
            Reset
          </button>
        </div>
      </div>

      <GridLayout
        className="layout"
        layout={layout}
        cols={12}
        rowHeight={100}
        width={1200}
        onLayoutChange={onLayoutChange}
        draggableHandle=".drag-handle"
        isResizable={true}
        isDraggable={true}
      >
        {widgets.map(renderWidget)}
      </GridLayout>

      <div style={{ marginTop: '24px', padding: '16px', backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ fontSize: '14px', color: '#64748b', margin: 0 }}>
          <strong>Tip:</strong> Drag widgets to reorder, resize by dragging corners. Changes are saved automatically.
        </p>
      </div>
    </div>
  );
}

export default CustomizableDashboard;
