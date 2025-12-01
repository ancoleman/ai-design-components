# Drag-and-Drop Patterns

## Table of Contents
- [Sortable Lists](#sortable-lists)
- [Grid Layouts](#grid-layouts)
- [Nested Containers](#nested-containers)
- [Auto-Scrolling](#auto-scrolling)
- [Multi-Select Dragging](#multi-select-dragging)

## Sortable Lists

### Vertical List Pattern

Most common drag-and-drop pattern for priority ordering, task lists, and sequential content.

**Implementation with dnd-kit:**

```tsx
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';

function VerticalSortableList({ items, onReorder }) {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragEnd(event) {
    const { active, over } = event;

    if (active.id !== over.id) {
      const oldIndex = items.findIndex(item => item.id === active.id);
      const newIndex = items.findIndex(item => item.id === over.id);
      onReorder(arrayMove(items, oldIndex, newIndex));
    }
  }

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        {/* Sortable items here */}
      </SortableContext>
    </DndContext>
  );
}
```

### Horizontal List Pattern

Used for tab reordering, carousel management, and timeline elements.

**Key Differences:**
- Use `horizontalListSortingStrategy` instead of vertical
- Adjust drag handle positioning (typically on edges)
- Consider touch scrolling conflicts on mobile

```tsx
import { horizontalListSortingStrategy } from '@dnd-kit/sortable';

// In SortableContext:
<SortableContext items={items} strategy={horizontalListSortingStrategy}>
  {/* Horizontal items */}
</SortableContext>
```

### Drag Handle Pattern

Provides explicit drag affordance while keeping content interactive.

```tsx
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

function SortableItem({ id, children }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style}>
      <button
        className="drag-handle"
        {...attributes}
        {...listeners}
        aria-label="Drag to reorder"
      >
        ⋮⋮
      </button>
      {children}
    </div>
  );
}
```

## Grid Layouts

### 2D Grid Pattern

For dashboard widgets, image galleries, and card layouts.

```tsx
import { rectSortingStrategy } from '@dnd-kit/sortable';

function GridLayout({ items, columns = 3 }) {
  return (
    <SortableContext items={items} strategy={rectSortingStrategy}>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${columns}, 1fr)`,
          gap: '1rem'
        }}
      >
        {items.map(item => (
          <SortableGridItem key={item.id} {...item} />
        ))}
      </div>
    </SortableContext>
  );
}
```

### Masonry Layout Pattern

For Pinterest-style layouts with variable heights.

**Considerations:**
- Calculate positions dynamically
- Handle reflow on drop
- Optimize for performance with many items

```tsx
// Use custom collision detection for masonry
function masonryCollisionDetection(args) {
  // Custom logic to handle variable heights
  // Consider item positions and sizes
  return closestCenter(args);
}
```

## Nested Containers

### Parent-Child Dragging

For tree structures, nested lists, and hierarchical content.

```tsx
function NestedSortable({ items, depth = 0 }) {
  const maxDepth = 3; // Prevent infinite nesting

  return (
    <SortableContext items={items}>
      {items.map(item => (
        <div key={item.id} style={{ marginLeft: depth * 20 }}>
          <SortableItem {...item} />
          {item.children && depth < maxDepth && (
            <NestedSortable items={item.children} depth={depth + 1} />
          )}
        </div>
      ))}
    </SortableContext>
  );
}
```

## Auto-Scrolling

### Edge Detection Pattern

Automatically scroll when dragging near container edges.

```tsx
import { AutoScrollActivator } from '@dnd-kit/auto-scroll';

function ScrollableList() {
  const autoScrollOptions = {
    canScroll: (element) => true,
    threshold: {
      x: 0.2, // 20% from edge
      y: 0.2,
    },
    maxSpeed: 10,
    acceleration: 10,
  };

  return (
    <DndContext autoScroll={autoScrollOptions}>
      {/* Scrollable content */}
    </DndContext>
  );
}
```

### Viewport Scrolling

For full-page draggable interfaces.

```tsx
// Enable window scrolling during drag
const sensors = useSensors(
  useSensor(PointerSensor, {
    activationConstraint: {
      distance: 8, // Prevent accidental drags
    },
  })
);

// Auto-scroll viewport
useEffect(() => {
  if (isDragging) {
    // Custom scroll logic based on cursor position
  }
}, [isDragging, cursorPosition]);
```

## Multi-Select Dragging

### Selection State Pattern

Allow dragging multiple items simultaneously.

```tsx
function MultiSelectDraggable() {
  const [selectedIds, setSelectedIds] = useState(new Set());

  function handleDragStart(event) {
    const { active } = event;

    if (!selectedIds.has(active.id)) {
      // If dragging unselected item, clear selection
      setSelectedIds(new Set([active.id]));
    }
    // Otherwise drag all selected items
  }

  function handleDragEnd(event) {
    const { active, over } = event;

    if (over && selectedIds.size > 0) {
      // Move all selected items relative to drop position
      const itemsToMove = Array.from(selectedIds);
      // Reorder logic here
    }
  }

  return (
    <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
      {/* Multi-selectable items */}
    </DndContext>
  );
}
```

### Visual Feedback for Multi-Select

```tsx
function MultiSelectItem({ id, isSelected, isDragging }) {
  const style = {
    backgroundColor: isSelected ? 'var(--color-primary-100)' : 'white',
    opacity: isDragging && isSelected ? 0.5 : 1,
    border: isSelected ? '2px solid var(--color-primary)' : '1px solid var(--color-border)',
  };

  return <div style={style}>{/* Content */}</div>;
}
```

## Common Patterns Summary

### Pattern Selection Guide

| Use Case | Pattern | Key Considerations |
|----------|---------|-------------------|
| Task lists | Vertical sortable | Drag handles, keyboard nav |
| Tabs | Horizontal sortable | Touch scrolling conflicts |
| Dashboard | Grid layout | Responsive columns |
| File browser | Nested containers | Depth limits |
| Kanban | Multi-container | Drop zones, auto-scroll |
| Batch operations | Multi-select | Visual selection state |

### Performance Tips

1. **Virtualization**: For lists >100 items
2. **Throttling**: Limit drag event frequency
3. **Memoization**: Prevent unnecessary re-renders
4. **CSS Transforms**: Use transform, not position
5. **Will-change**: Hint browser about animations

### Accessibility Requirements

Every pattern must include:
- Keyboard navigation support
- Screen reader announcements
- Focus management
- Alternative UI options
- Clear visual feedback

### Mobile Considerations

- Long press (300ms) to initiate drag
- Prevent scroll during drag
- Larger touch targets (44px minimum)
- Handle gesture conflicts
- Test on actual devices