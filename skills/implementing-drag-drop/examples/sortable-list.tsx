import React, { useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

// Item interface
interface TodoItem {
  id: string;
  text: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
}

// Sortable item component
function SortableItem({ item }: { item: TodoItem }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`sortable-item priority-${item.priority} ${item.completed ? 'completed' : ''}`}
    >
      {/* Drag handle */}
      <button
        className="drag-handle"
        {...attributes}
        {...listeners}
        aria-label={`Drag to reorder ${item.text}`}
      >
        <svg width="20" height="20" viewBox="0 0 20 20">
          <g fill="currentColor">
            <circle cx="7" cy="5" r="1.5" />
            <circle cx="13" cy="5" r="1.5" />
            <circle cx="7" cy="10" r="1.5" />
            <circle cx="13" cy="10" r="1.5" />
            <circle cx="7" cy="15" r="1.5" />
            <circle cx="13" cy="15" r="1.5" />
          </g>
        </svg>
      </button>

      {/* Checkbox */}
      <input
        type="checkbox"
        checked={item.completed}
        onChange={() => {/* Toggle completion */}}
        aria-label={`Mark ${item.text} as ${item.completed ? 'incomplete' : 'complete'}`}
      />

      {/* Item text */}
      <span className="item-text">{item.text}</span>

      {/* Priority badge */}
      <span className={`priority-badge priority-${item.priority}`}>
        {item.priority}
      </span>

      {/* Alternative move buttons (for accessibility) */}
      <div className="alternative-controls">
        <button
          onClick={() => {/* Move up logic */}}
          aria-label={`Move ${item.text} up`}
          className="move-btn"
        >
          ↑
        </button>
        <button
          onClick={() => {/* Move down logic */}}
          aria-label={`Move ${item.text} down`}
          className="move-btn"
        >
          ↓
        </button>
      </div>
    </div>
  );
}

// Main sortable list component
export function SortableList() {
  const [items, setItems] = useState<TodoItem[]>([
    { id: '1', text: 'Complete project documentation', completed: false, priority: 'high' },
    { id: '2', text: 'Review pull requests', completed: true, priority: 'medium' },
    { id: '3', text: 'Update dependencies', completed: false, priority: 'low' },
    { id: '4', text: 'Write unit tests', completed: false, priority: 'high' },
    { id: '5', text: 'Deploy to staging', completed: false, priority: 'medium' },
  ]);

  // Configure sensors for keyboard and pointer
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement required to start drag
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Handle drag end
  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      setItems((items) => {
        const oldIndex = items.findIndex((item) => item.id === active.id);
        const newIndex = items.findIndex((item) => item.id === over.id);

        const newItems = arrayMove(items, oldIndex, newIndex);

        // Announce change to screen readers
        announceReorder(items[oldIndex], oldIndex + 1, newIndex + 1);

        return newItems;
      });
    }
  }

  // Screen reader announcement
  function announceReorder(item: TodoItem, fromPosition: number, toPosition: number) {
    const announcement = `${item.text} moved from position ${fromPosition} to position ${toPosition}`;
    const liveRegion = document.getElementById('drag-drop-announcements');
    if (liveRegion) {
      liveRegion.textContent = announcement;
    }
  }

  return (
    <div className="sortable-list-container">
      <h2>Todo List (Drag to Reorder)</h2>

      {/* Screen reader instructions */}
      <div id="drag-instructions" className="sr-only">
        To reorder items: Press Tab to navigate to an item's drag handle,
        press Space or Enter to lift the item, use Arrow keys to move it,
        and press Space or Enter again to drop it in the new position.
        Press Escape to cancel the drag operation.
      </div>

      {/* Live region for announcements */}
      <div
        id="drag-drop-announcements"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      />

      {/* Sortable list */}
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={items}
          strategy={verticalListSortingStrategy}
        >
          <div
            role="list"
            aria-label="Sortable todo list"
            aria-describedby="drag-instructions"
          >
            {items.map((item, index) => (
              <div
                key={item.id}
                role="listitem"
                aria-setsize={items.length}
                aria-posinset={index + 1}
              >
                <SortableItem item={item} />
              </div>
            ))}
          </div>
        </SortableContext>
      </DndContext>

      {/* Summary */}
      <div className="list-summary">
        <p>Total: {items.length} items</p>
        <p>Completed: {items.filter(i => i.completed).length}</p>
        <p>High Priority: {items.filter(i => i.priority === 'high').length}</p>
      </div>
    </div>
  );
}

// Styles (using CSS-in-JS or external stylesheet)
const styles = `
.sortable-list-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

.sortable-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.sortable-item:hover {
  box-shadow: var(--shadow-sm);
}

.sortable-item.completed {
  opacity: 0.6;
}

.sortable-item.completed .item-text {
  text-decoration: line-through;
}

.drag-handle {
  cursor: grab;
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: var(--color-text-tertiary);
  transition: all 0.2s;
}

.drag-handle:hover {
  background: var(--color-gray-100);
  border-radius: var(--radius-sm);
}

.drag-handle:active {
  cursor: grabbing;
}

.item-text {
  flex: 1;
  font-size: 1rem;
}

.priority-badge {
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.priority-low {
  background: var(--color-blue-100);
  color: var(--color-blue-700);
}

.priority-medium {
  background: var(--color-yellow-100);
  color: var(--color-yellow-700);
}

.priority-high {
  background: var(--color-red-100);
  color: var(--color-red-700);
}

.alternative-controls {
  display: flex;
  gap: 0.25rem;
}

.move-btn {
  padding: 0.25rem 0.5rem;
  background: var(--color-gray-100);
  border: 1px solid var(--color-gray-300);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.move-btn:hover {
  background: var(--color-gray-200);
}

.move-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.list-summary {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  gap: 2rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

/* Accessibility: Screen reader only content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Focus styles */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Dragging state */
.sortable-item[aria-grabbed="true"] {
  box-shadow: var(--shadow-lg);
  transform: scale(1.02);
}

/* Mobile responsive */
@media (max-width: 640px) {
  .sortable-item {
    padding: 0.75rem;
  }

  .drag-handle {
    padding: 0.75rem;
  }

  .alternative-controls {
    display: flex; /* Always show on mobile */
  }
}

@media (min-width: 641px) {
  .alternative-controls {
    display: none; /* Hide on desktop, show on hover/focus */
  }

  .sortable-item:hover .alternative-controls,
  .sortable-item:focus-within .alternative-controls {
    display: flex;
  }
}
`;