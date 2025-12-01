import React, { useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  rectSortingStrategy,
} from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

// Widget interface
interface Widget {
  id: string;
  title: string;
  content: React.ReactNode;
  size: 'small' | 'medium' | 'large';
  color: string;
  icon: string;
}

// Grid item component
function GridItem({
  widget,
  isDragging,
}: {
  widget: Widget;
  isDragging?: boolean;
}) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: localIsDragging,
  } = useSortable({ id: widget.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging || localIsDragging ? 0.5 : 1,
    gridColumn: widget.size === 'large' ? 'span 2' : 'span 1',
    gridRow: widget.size === 'large' ? 'span 2' : 'span 1',
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`grid-item size-${widget.size}`}
      {...attributes}
      {...listeners}
    >
      <div
        className="widget"
        style={{ background: `linear-gradient(135deg, ${widget.color}22, ${widget.color}44)` }}
      >
        <div className="widget-header">
          <span className="widget-icon">{widget.icon}</span>
          <h3 className="widget-title">{widget.title}</h3>
          <button className="widget-menu" aria-label="Widget menu">
            ⋮
          </button>
        </div>

        <div className="widget-content">
          {widget.content}
        </div>

        {/* Resize handle */}
        <button
          className="resize-handle"
          aria-label="Resize widget"
          onClick={(e) => {
            e.stopPropagation();
            // Handle resize
          }}
        >
          ⤡
        </button>
      </div>
    </div>
  );
}

// Main grid component
export function GridReorder() {
  const [widgets, setWidgets] = useState<Widget[]>([
    {
      id: 'widget-1',
      title: 'Analytics',
      content: (
        <div className="chart-placeholder">
          <div className="bar" style={{ height: '60%' }}></div>
          <div className="bar" style={{ height: '80%' }}></div>
          <div className="bar" style={{ height: '40%' }}></div>
          <div className="bar" style={{ height: '90%' }}></div>
          <div className="bar" style={{ height: '70%' }}></div>
        </div>
      ),
      size: 'large',
      color: '#3b82f6',
      icon: '📊',
    },
    {
      id: 'widget-2',
      title: 'Users',
      content: <div className="metric">1,234</div>,
      size: 'small',
      color: '#10b981',
      icon: '👥',
    },
    {
      id: 'widget-3',
      title: 'Revenue',
      content: <div className="metric">$54,321</div>,
      size: 'small',
      color: '#f59e0b',
      icon: '💰',
    },
    {
      id: 'widget-4',
      title: 'Activity',
      content: (
        <div className="activity-list">
          <div className="activity-item">User signed up</div>
          <div className="activity-item">New order received</div>
          <div className="activity-item">Payment processed</div>
        </div>
      ),
      size: 'medium',
      color: '#8b5cf6',
      icon: '📈',
    },
    {
      id: 'widget-5',
      title: 'Tasks',
      content: (
        <div className="task-progress">
          <div className="progress-item">
            <span>In Progress</span>
            <span>5</span>
          </div>
          <div className="progress-item">
            <span>Completed</span>
            <span>12</span>
          </div>
        </div>
      ),
      size: 'small',
      color: '#ef4444',
      icon: '✓',
    },
    {
      id: 'widget-6',
      title: 'Calendar',
      content: (
        <div className="mini-calendar">
          <div className="calendar-header">November 2024</div>
          <div className="calendar-grid">
            {[...Array(30)].map((_, i) => (
              <div key={i} className="calendar-day">
                {i + 1}
              </div>
            ))}
          </div>
        </div>
      ),
      size: 'medium',
      color: '#ec4899',
      icon: '📅',
    },
  ]);

  const [activeId, setActiveId] = useState<string | null>(null);
  const [columns, setColumns] = useState(4);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 10,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragStart(event: DragStartEvent) {
    setActiveId(event.active.id as string);
  }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      setWidgets((items) => {
        const oldIndex = items.findIndex((item) => item.id === active.id);
        const newIndex = items.findIndex((item) => item.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }

    setActiveId(null);
  }

  // Responsive columns
  const handleColumnChange = (newColumns: number) => {
    setColumns(newColumns);
  };

  const activeWidget = activeId
    ? widgets.find((w) => w.id === activeId)
    : null;

  return (
    <div className="grid-container">
      <div className="grid-header">
        <h2>Dashboard Grid</h2>

        <div className="grid-controls">
          <div className="column-selector">
            <label>Columns:</label>
            <button
              onClick={() => handleColumnChange(2)}
              className={columns === 2 ? 'active' : ''}
              aria-label="2 columns"
            >
              2
            </button>
            <button
              onClick={() => handleColumnChange(3)}
              className={columns === 3 ? 'active' : ''}
              aria-label="3 columns"
            >
              3
            </button>
            <button
              onClick={() => handleColumnChange(4)}
              className={columns === 4 ? 'active' : ''}
              aria-label="4 columns"
            >
              4
            </button>
          </div>

          <button className="add-widget-btn">
            + Add Widget
          </button>
        </div>
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={widgets}
          strategy={rectSortingStrategy}
        >
          <div
            className="widget-grid"
            style={{
              gridTemplateColumns: `repeat(${columns}, 1fr)`,
            }}
          >
            {widgets.map((widget) => (
              <GridItem key={widget.id} widget={widget} />
            ))}
          </div>
        </SortableContext>

        <DragOverlay>
          {activeWidget && (
            <GridItem widget={activeWidget} isDragging />
          )}
        </DragOverlay>
      </DndContext>

      {/* Instructions */}
      <div className="grid-instructions">
        <p>
          <strong>Drag widgets</strong> to reorder •
          <strong> Resize</strong> using corner handle •
          <strong> Keyboard</strong>: Tab to focus, Space to grab, Arrows to move
        </p>
      </div>
    </div>
  );
}

// Styles
const styles = `
.grid-container {
  padding: 2rem;
  background: var(--color-gray-50);
  min-height: 100vh;
}

.grid-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.grid-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.column-selector {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.column-selector label {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.column-selector button {
  padding: 0.5rem 0.75rem;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all 0.2s;
}

.column-selector button:hover {
  background: var(--color-gray-100);
}

.column-selector button.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.add-widget-btn {
  padding: 0.5rem 1rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.add-widget-btn:hover {
  background: var(--color-primary-600);
}

.widget-grid {
  display: grid;
  gap: 1rem;
  grid-auto-rows: minmax(120px, 1fr);
  grid-auto-flow: dense;
}

.grid-item {
  cursor: grab;
  transition: transform 0.2s, opacity 0.2s;
}

.grid-item:active {
  cursor: grabbing;
}

.widget {
  height: 100%;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.2s;
}

.widget:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.widget-icon {
  font-size: 1.25rem;
}

.widget-title {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0;
}

.widget-menu {
  padding: 0.25rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--color-text-tertiary);
}

.widget-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.resize-handle {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  width: 1.5rem;
  height: 1.5rem;
  background: transparent;
  border: none;
  cursor: nwse-resize;
  color: var(--color-text-tertiary);
  opacity: 0;
  transition: opacity 0.2s;
}

.widget:hover .resize-handle {
  opacity: 1;
}

/* Widget content styles */
.metric {
  font-size: 2rem;
  font-weight: bold;
  color: var(--color-text-primary);
}

.chart-placeholder {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
  height: 100px;
  width: 100%;
}

.bar {
  flex: 1;
  background: var(--color-primary-400);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.activity-list {
  width: 100%;
  font-size: 0.813rem;
}

.activity-item {
  padding: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.task-progress {
  width: 100%;
}

.progress-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  font-size: 0.875rem;
}

.mini-calendar {
  width: 100%;
  font-size: 0.75rem;
}

.calendar-header {
  text-align: center;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-gray-50);
  border-radius: 2px;
  font-size: 0.625rem;
}

.grid-instructions {
  margin-top: 2rem;
  padding: 1rem;
  background: var(--color-white);
  border-radius: var(--radius-md);
  text-align: center;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

/* Responsive */
@media (max-width: 768px) {
  .widget-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }

  .grid-item.size-large {
    grid-column: span 2;
  }
}

@media (max-width: 480px) {
  .widget-grid {
    grid-template-columns: 1fr !important;
  }

  .grid-item.size-large,
  .grid-item.size-medium {
    grid-column: span 1;
    grid-row: span 1;
  }
}

/* Drag overlay */
.grid-item[aria-grabbed="true"] {
  opacity: 0.5;
}

/* Focus styles */
.grid-item:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
`;