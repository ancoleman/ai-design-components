# Drag-and-Drop Library Guide

## Table of Contents
- [Library Comparison](#library-comparison)
- [dnd-kit Setup](#dnd-kit-setup)
- [Core Concepts](#core-concepts)
- [Migration Guide](#migration-guide)
- [Alternative Libraries](#alternative-libraries)

## Library Comparison

### Current Landscape (2025)

| Library | Status | Bundle Size | Accessibility | TypeScript | Best For |
|---------|--------|------------|---------------|------------|----------|
| **@dnd-kit** | ✅ Active | ~10KB core | ⭐⭐⭐⭐⭐ | Native | Modern React apps |
| react-beautiful-dnd | ⚠️ Archived | ~30KB | ⭐⭐⭐⭐ | Yes | Legacy projects |
| react-dnd | ✅ Active | ~20KB | ⭐⭐⭐ | Yes | Complex interactions |
| Pragmatic drag-drop | ✅ Active | ~5KB | ⭐⭐⭐⭐ | Native | Atlassian products |
| SortableJS | ✅ Active | ~27KB | ⭐⭐ | No | Vanilla JS |

**Note:** react-beautiful-dnd was archived in August 2025. Migrate to dnd-kit or Pragmatic drag-drop.

## dnd-kit Setup

### Installation

```bash
# Core packages
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities

# Optional packages
npm install @dnd-kit/modifiers   # Advanced drag modifiers
npm install @dnd-kit/accessibility  # Enhanced accessibility
```

### Basic Setup

```tsx
// 1. Import required components
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy
} from '@dnd-kit/sortable';

// 2. Configure sensors
const sensors = useSensors(
  useSensor(PointerSensor, {
    activationConstraint: {
      distance: 8, // Prevent accidental activation
    },
  }),
  useSensor(KeyboardSensor, {
    coordinateGetter: sortableKeyboardCoordinates,
  })
);

// 3. Set up context
function App() {
  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      {/* Your draggable content */}
    </DndContext>
  );
}
```

### TypeScript Configuration

```typescript
// types/dnd.ts
import type { Active, Over } from '@dnd-kit/core';

export interface DragEndEvent {
  active: Active;
  over: Over | null;
}

export interface DraggableItem {
  id: string;
  content: React.ReactNode;
  order?: number;
}

export interface DragState {
  activeId: string | null;
  overId: string | null;
  isDragging: boolean;
}
```

## Core Concepts

### Sensors

Sensors detect different input methods for initiating drag operations.

```tsx
// Pointer Sensor - Mouse and touch
useSensor(PointerSensor, {
  activationConstraint: {
    distance: 8, // Movement threshold
    delay: 250,  // Long press for touch
    tolerance: 5, // Movement tolerance during delay
  },
});

// Keyboard Sensor - Accessibility
useSensor(KeyboardSensor, {
  coordinateGetter: sortableKeyboardCoordinates,
  scrollBehavior: 'smooth',
});

// Custom Touch Sensor
class TouchSensor extends PointerSensor {
  static activators = [
    {
      eventName: 'onTouchStart',
      handler: ({ nativeEvent: event }) => {
        return event.touches.length === 1;
      },
    },
  ];
}
```

### Collision Detection

Algorithms to determine drop targets.

```tsx
import {
  closestCenter,     // Closest to center point
  closestCorners,    // Closest to any corner
  rectIntersection,  // Rectangle intersection
  pointerWithin,     // Pointer within bounds
} from '@dnd-kit/core';

// Custom collision detection
function customCollisionDetection(args) {
  // First try pointer within
  const pointerCollisions = pointerWithin(args);
  if (pointerCollisions.length > 0) {
    return pointerCollisions;
  }
  // Fallback to closest center
  return closestCenter(args);
}
```

### Modifiers

Transform drag behavior.

```tsx
import { restrictToVerticalAxis, restrictToWindowEdges } from '@dnd-kit/modifiers';

<DndContext modifiers={[restrictToVerticalAxis, restrictToWindowEdges]}>
  {/* Constrained dragging */}
</DndContext>
```

### Drag Overlay

Custom drag preview.

```tsx
import { DragOverlay } from '@dnd-kit/core';

function App() {
  const [activeId, setActiveId] = useState(null);

  return (
    <DndContext onDragStart={({active}) => setActiveId(active.id)}>
      {/* Regular content */}
      <DragOverlay>
        {activeId ? <CustomDragPreview id={activeId} /> : null}
      </DragOverlay>
    </DndContext>
  );
}
```

## Migration Guide

### From react-beautiful-dnd to dnd-kit

#### Key Differences

| Feature | react-beautiful-dnd | dnd-kit |
|---------|-------------------|---------|
| API Style | Higher-level | Lower-level, composable |
| Drag Preview | Built-in | Custom via DragOverlay |
| Animation | Automatic | Manual control |
| Accessibility | Good | Excellent |
| Touch Support | Basic | Advanced |

#### Migration Steps

**1. Replace Imports**

```tsx
// Before (react-beautiful-dnd)
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

// After (dnd-kit)
import { DndContext, SortableContext, useSortable } from '@dnd-kit/sortable';
```

**2. Update Context Structure**

```tsx
// Before
<DragDropContext onDragEnd={onDragEnd}>
  <Droppable droppableId="list">
    {(provided) => (
      <div {...provided.droppableProps} ref={provided.innerRef}>
        {items.map((item, index) => (
          <Draggable key={item.id} draggableId={item.id} index={index}>
            {(provided, snapshot) => (
              <div
                ref={provided.innerRef}
                {...provided.draggableProps}
                {...provided.dragHandleProps}
              >
                {item.content}
              </div>
            )}
          </Draggable>
        ))}
        {provided.placeholder}
      </div>
    )}
  </Droppable>
</DragDropContext>

// After
<DndContext sensors={sensors} onDragEnd={handleDragEnd}>
  <SortableContext items={items}>
    {items.map(item => (
      <SortableItem key={item.id} id={item.id}>
        {item.content}
      </SortableItem>
    ))}
  </SortableContext>
</DndContext>
```

**3. Create Sortable Item Component**

```tsx
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
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {children}
    </div>
  );
}
```

**4. Update Event Handlers**

```tsx
// Before
function onDragEnd(result) {
  if (!result.destination) return;

  const items = Array.from(this.state.items);
  const [reorderedItem] = items.splice(result.source.index, 1);
  items.splice(result.destination.index, 0, reorderedItem);

  this.setState({ items });
}

// After
function handleDragEnd(event) {
  const { active, over } = event;

  if (active.id !== over.id) {
    setItems((items) => {
      const oldIndex = items.findIndex(item => item.id === active.id);
      const newIndex = items.findIndex(item => item.id === over.id);
      return arrayMove(items, oldIndex, newIndex);
    });
  }
}
```

## Alternative Libraries

### react-dnd

**When to Use:**
- Complex drag sources and drop targets
- Need HTML5 backend flexibility
- Custom drag layers

**Setup:**
```tsx
import { useDrag, useDrop, DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

function App() {
  return (
    <DndProvider backend={HTML5Backend}>
      {/* Your app */}
    </DndProvider>
  );
}
```

### Pragmatic drag-drop (Atlassian)

**When to Use:**
- Minimal bundle size priority
- Atlassian ecosystem
- Simple drag operations

**Setup:**
```tsx
import { draggable, dropTargetForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter';

// Make element draggable
useEffect(() => {
  const element = ref.current;
  if (!element) return;

  return draggable({
    element,
    getInitialData: () => ({ id: item.id }),
  });
}, [item.id]);
```

### SortableJS

**When to Use:**
- Vanilla JavaScript projects
- Framework agnostic
- Legacy browser support

**Note:** Limited accessibility support and no TypeScript.

## Best Practices

### Performance Optimization

```tsx
// 1. Memoize expensive calculations
const sortedItems = useMemo(
  () => items.sort((a, b) => a.order - b.order),
  [items]
);

// 2. Use CSS transforms
const style = {
  transform: `translate3d(${x}px, ${y}px, 0)`,
  willChange: 'transform',
};

// 3. Throttle drag events
const throttledDragMove = useThrottle(handleDragMove, 16); // 60fps
```

### Accessibility First

```tsx
// Always provide keyboard support
const sensors = useSensors(
  useSensor(PointerSensor),
  useSensor(KeyboardSensor, {
    coordinateGetter: sortableKeyboardCoordinates,
  })
);

// Add ARIA attributes
<div
  role="button"
  tabIndex={0}
  aria-roledescription="sortable"
  aria-describedby="DndContext-announcements"
/>
```

### Touch Device Support

```tsx
// Configure touch activation
useSensor(PointerSensor, {
  activationConstraint: {
    delay: 250, // Long press
    tolerance: 5, // Movement tolerance
  },
});

// Prevent scrolling during drag
useEffect(() => {
  if (isDragging) {
    document.body.style.overflow = 'hidden';
    document.body.style.touchAction = 'none';
  }
  return () => {
    document.body.style.overflow = '';
    document.body.style.touchAction = '';
  };
}, [isDragging]);
```

## Troubleshooting

### Common Issues

**Issue: Drag not initiating on touch devices**
- Solution: Add delay to activation constraint
- Check for conflicting touch handlers

**Issue: Performance lag with many items**
- Solution: Implement virtualization
- Use CSS transforms instead of position
- Memoize components

**Issue: Accessibility not working**
- Solution: Ensure keyboard sensor configured
- Add proper ARIA attributes
- Test with screen readers

**Issue: Scroll not working during drag**
- Solution: Configure auto-scroll
- Check overflow styles
- Implement edge detection