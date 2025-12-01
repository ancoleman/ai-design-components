# Performance Optimization for Drag-and-Drop

## Table of Contents
- [Virtual Scrolling](#virtual-scrolling)
- [Throttling and Debouncing](#throttling-and-debouncing)
- [CSS Optimization](#css-optimization)
- [React Optimization](#react-optimization)
- [Large Dataset Handling](#large-dataset-handling)
- [Memory Management](#memory-management)

## Virtual Scrolling

### Virtual List with Drag-and-Drop

```tsx
import { VariableSizeList } from 'react-window';
import { DndContext, useSortable } from '@dnd-kit/sortable';

interface VirtualDragListProps {
  items: any[];
  itemHeight: number | ((index: number) => number);
  height: number;
  onReorder: (items: any[]) => void;
}

function VirtualDragList({ items, itemHeight, height, onReorder }: VirtualDragListProps) {
  // Track visible items for drag operations
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 10 });

  const Row = ({ index, style, data }) => {
    const item = data[index];

    return (
      <div style={style}>
        <VirtualDraggableItem item={item} index={index} />
      </div>
    );
  };

  const handleScroll = ({ visibleStartIndex, visibleStopIndex }) => {
    setVisibleRange({ start: visibleStartIndex, end: visibleStopIndex });
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <VariableSizeList
        height={height}
        itemCount={items.length}
        itemSize={itemHeight}
        width="100%"
        itemData={items}
        onItemsRendered={handleScroll}
        overscanCount={5} // Render extra items for smoother scrolling
      >
        {Row}
      </VariableSizeList>
    </DndContext>
  );
}

// Optimized draggable item for virtual list
const VirtualDraggableItem = memo(({ item, index }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: item.id,
    disabled: false,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    // Use transform for positioning, not top/left
    position: 'relative' as const,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="virtual-draggable-item"
    >
      {item.content}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison for memoization
  return prevProps.item.id === nextProps.item.id &&
         prevProps.item.content === nextProps.item.content &&
         prevProps.index === nextProps.index;
});
```

### Intersection Observer for Lazy Loading

```tsx
function LazyLoadDragList({ items, onLoadMore }) {
  const [visibleItems, setVisibleItems] = useState(items.slice(0, 50));
  const loaderRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (entry.isIntersecting && visibleItems.length < items.length) {
          // Load more items
          const nextBatch = items.slice(
            visibleItems.length,
            visibleItems.length + 50
          );
          setVisibleItems(prev => [...prev, ...nextBatch]);
        }
      },
      {
        root: null,
        rootMargin: '100px', // Start loading before reaching the end
        threshold: 0.1,
      }
    );

    if (loaderRef.current) {
      observer.observe(loaderRef.current);
    }

    return () => observer.disconnect();
  }, [items, visibleItems]);

  return (
    <div className="lazy-load-container">
      <DndContext>
        <SortableContext items={visibleItems}>
          {visibleItems.map(item => (
            <SortableItem key={item.id} item={item} />
          ))}
        </SortableContext>
      </DndContext>

      {visibleItems.length < items.length && (
        <div ref={loaderRef} className="loading-indicator">
          Loading more items...
        </div>
      )}
    </div>
  );
}
```

## Throttling and Debouncing

### Throttled Drag Updates

```tsx
function useThrottle<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): T {
  const lastCall = useRef(0);
  const timeoutRef = useRef<NodeJS.Timeout>();

  return useCallback((...args: Parameters<T>) => {
    const now = Date.now();

    if (now - lastCall.current >= delay) {
      lastCall.current = now;
      callback(...args);
    } else {
      // Schedule for later
      clearTimeout(timeoutRef.current);
      timeoutRef.current = setTimeout(() => {
        lastCall.current = Date.now();
        callback(...args);
      }, delay - (now - lastCall.current));
    }
  }, [callback, delay]) as T;
}

// Usage in drag handler
function OptimizedDragHandler() {
  const [dragPosition, setDragPosition] = useState({ x: 0, y: 0 });

  // Throttle to 60fps (16ms) for smooth animation
  const throttledUpdatePosition = useThrottle((position) => {
    setDragPosition(position);
    // Expensive calculations here
  }, 16);

  const handleDragMove = (event) => {
    const { active } = event;
    throttledUpdatePosition({
      x: active.rect.current.translated.left,
      y: active.rect.current.translated.top,
    });
  };

  return (
    <DndContext onDragMove={handleDragMove}>
      {/* Content */}
    </DndContext>
  );
}
```

### Debounced Auto-Save

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Auto-save after drag operations
function AutoSaveDragList({ items, onSave }) {
  const [localItems, setLocalItems] = useState(items);
  const debouncedItems = useDebounce(localItems, 500);

  useEffect(() => {
    if (debouncedItems !== items) {
      onSave(debouncedItems);
    }
  }, [debouncedItems]);

  const handleDragEnd = (event) => {
    // Update local state immediately
    const newItems = reorderItems(localItems, event);
    setLocalItems(newItems);
    // Debounced save will trigger after 500ms of no changes
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      {/* Draggable items */}
    </DndContext>
  );
}
```

## CSS Optimization

### High-Performance CSS

```css
/* Use transform instead of position for smooth animations */
.draggable-item {
  transform: translate3d(0, 0, 0); /* Enable GPU acceleration */
  will-change: transform; /* Hint browser optimization */
  backface-visibility: hidden; /* Prevent flickering */
  perspective: 1000px; /* Create stacking context */
}

/* Optimize transitions */
.draggable-item-transition {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
  transition-property: transform; /* Only animate what changes */
}

/* Reduce paint areas during drag */
.dragging {
  pointer-events: none; /* Prevent hover effects */
  z-index: 9999; /* Lift above other elements */
  position: fixed; /* Take out of document flow */
}

/* Optimize shadows (expensive to render) */
.draggable-item {
  /* Use box-shadow sparingly */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dragging .draggable-item {
  /* Larger shadow only when dragging */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* Use CSS containment */
.drag-container {
  contain: layout style; /* Isolate layout recalculations */
}

/* Optimize hover states */
@media (hover: hover) {
  .draggable-item:hover {
    /* Only apply hover on devices that support it */
    background-color: var(--hover-color);
  }
}

/* Reduce visual complexity during drag */
.drag-container.is-dragging .draggable-item:not(.dragging) {
  opacity: 0.7; /* Dim non-dragged items */
  filter: grayscale(30%); /* Reduce visual noise */
}
```

### CSS Transform Utilities

```tsx
// Utility for efficient transforms
export const transformStyles = {
  translate: (x: number, y: number, scale = 1) => ({
    transform: `translate3d(${x}px, ${y}px, 0) scale(${scale})`,
    WebkitTransform: `translate3d(${x}px, ${y}px, 0) scale(${scale})`,
  }),

  rotate: (deg: number) => ({
    transform: `rotate(${deg}deg)`,
    WebkitTransform: `rotate(${deg}deg)`,
  }),

  // Combine transforms efficiently
  combine: (...transforms: string[]) => ({
    transform: transforms.join(' '),
    WebkitTransform: transforms.join(' '),
  }),
};

// Use requestAnimationFrame for smooth animations
export function animateTransform(
  element: HTMLElement,
  from: { x: number; y: number },
  to: { x: number; y: number },
  duration: number,
  onComplete?: () => void
) {
  const startTime = performance.now();

  const animate = (currentTime: number) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Easing function
    const easeProgress = 1 - Math.pow(1 - progress, 3);

    const x = from.x + (to.x - from.x) * easeProgress;
    const y = from.y + (to.y - from.y) * easeProgress;

    element.style.transform = `translate3d(${x}px, ${y}px, 0)`;

    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      onComplete?.();
    }
  };

  requestAnimationFrame(animate);
}
```

## React Optimization

### Memoization Strategies

```tsx
// Memoize expensive components
const MemoizedDraggableItem = memo(
  ({ item, index, onDragEnd }) => {
    const {
      attributes,
      listeners,
      setNodeRef,
      transform,
      transition,
    } = useSortable({ id: item.id });

    return (
      <div
        ref={setNodeRef}
        style={{
          transform: CSS.Transform.toString(transform),
          transition,
        }}
        {...attributes}
        {...listeners}
      >
        {item.content}
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Custom equality check
    return (
      prevProps.item.id === nextProps.item.id &&
      prevProps.item.content === nextProps.item.content &&
      prevProps.index === nextProps.index
    );
  }
);

// Memoize callbacks
function DragListContainer({ items }) {
  const handleDragEnd = useCallback((event) => {
    const { active, over } = event;
    if (active.id !== over.id) {
      // Reorder logic
    }
  }, []); // Empty deps if function doesn't depend on props

  const sensors = useMemo(
    () => [
      useSensor(PointerSensor),
      useSensor(KeyboardSensor),
    ],
    []
  );

  return (
    <DndContext sensors={sensors} onDragEnd={handleDragEnd}>
      {/* Content */}
    </DndContext>
  );
}
```

### State Management Optimization

```tsx
// Use local state for drag preview, global for final position
function OptimizedDragState({ initialItems }) {
  const [items, setItems] = useState(initialItems);
  const [dragPreview, setDragPreview] = useState(null);
  const [activeId, setActiveId] = useState(null);

  const handleDragStart = (event) => {
    setActiveId(event.active.id);
    // Don't update main state yet
    setDragPreview({
      id: event.active.id,
      position: { x: 0, y: 0 },
    });
  };

  const handleDragMove = (event) => {
    // Only update preview position (cheap)
    setDragPreview(prev => ({
      ...prev,
      position: {
        x: event.delta.x,
        y: event.delta.y,
      },
    }));
  };

  const handleDragEnd = (event) => {
    // Update main state once (expensive)
    if (event.over && event.active.id !== event.over.id) {
      setItems(prevItems => {
        const oldIndex = prevItems.findIndex(i => i.id === event.active.id);
        const newIndex = prevItems.findIndex(i => i.id === event.over.id);
        return arrayMove(prevItems, oldIndex, newIndex);
      });
    }

    // Clean up
    setDragPreview(null);
    setActiveId(null);
  };

  return (
    <DndContext
      onDragStart={handleDragStart}
      onDragMove={handleDragMove}
      onDragEnd={handleDragEnd}
    >
      {/* Render items */}
      {/* Render preview overlay if dragging */}
    </DndContext>
  );
}
```

## Large Dataset Handling

### Chunked Rendering

```tsx
function ChunkedDragList({ items, chunkSize = 20 }) {
  const [renderedChunks, setRenderedChunks] = useState(1);

  useEffect(() => {
    // Progressively render chunks
    const timer = setTimeout(() => {
      if (renderedChunks * chunkSize < items.length) {
        setRenderedChunks(prev => prev + 1);
      }
    }, 0);

    return () => clearTimeout(timer);
  }, [renderedChunks, items.length, chunkSize]);

  const visibleItems = items.slice(0, renderedChunks * chunkSize);

  return (
    <div className="chunked-list">
      {visibleItems.map(item => (
        <DraggableItem key={item.id} item={item} />
      ))}

      {visibleItems.length < items.length && (
        <div className="loading-more">
          Rendering {visibleItems.length} of {items.length} items...
        </div>
      )}
    </div>
  );
}
```

### Indexed Data Structure

```tsx
// Use Map for O(1) lookups instead of Array.find
function useIndexedItems(initialItems: Item[]) {
  const [itemsMap, setItemsMap] = useState(() => {
    const map = new Map<string, Item>();
    initialItems.forEach(item => map.set(item.id, item));
    return map;
  });

  const [itemOrder, setItemOrder] = useState(() =>
    initialItems.map(item => item.id)
  );

  const items = useMemo(
    () => itemOrder.map(id => itemsMap.get(id)!).filter(Boolean),
    [itemOrder, itemsMap]
  );

  const moveItem = useCallback((fromId: string, toId: string) => {
    setItemOrder(prev => {
      const fromIndex = prev.indexOf(fromId);
      const toIndex = prev.indexOf(toId);
      if (fromIndex === -1 || toIndex === -1) return prev;

      const newOrder = [...prev];
      const [removed] = newOrder.splice(fromIndex, 1);
      newOrder.splice(toIndex, 0, removed);
      return newOrder;
    });
  }, []);

  const updateItem = useCallback((id: string, updates: Partial<Item>) => {
    setItemsMap(prev => {
      const newMap = new Map(prev);
      const item = newMap.get(id);
      if (item) {
        newMap.set(id, { ...item, ...updates });
      }
      return newMap;
    });
  }, []);

  return { items, moveItem, updateItem };
}
```

## Memory Management

### Cleanup and Prevention

```tsx
function useDragDropCleanup() {
  const activeRefs = useRef<Set<HTMLElement>>(new Set());
  const observers = useRef<Set<IntersectionObserver>>(new Set());

  const registerElement = useCallback((element: HTMLElement) => {
    activeRefs.current.add(element);

    return () => {
      activeRefs.current.delete(element);
      // Clean up any attached data
      delete (element as any)._dragData;
    };
  }, []);

  const createObserver = useCallback((callback: IntersectionObserverCallback) => {
    const observer = new IntersectionObserver(callback);
    observers.current.add(observer);

    return observer;
  }, []);

  useEffect(() => {
    return () => {
      // Cleanup all refs
      activeRefs.current.forEach(element => {
        delete (element as any)._dragData;
      });
      activeRefs.current.clear();

      // Disconnect all observers
      observers.current.forEach(observer => observer.disconnect());
      observers.current.clear();
    };
  }, []);

  return { registerElement, createObserver };
}
```

### Memory-Efficient File Handling

```tsx
function useFilePreview(file: File | null) {
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    if (!file || !file.type.startsWith('image/')) {
      setPreview(null);
      return;
    }

    // Create preview URL
    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);

    // Cleanup function
    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  return preview;
}

// Batch cleanup for multiple files
function useBatchFileCleanup() {
  const urlsRef = useRef<Set<string>>(new Set());

  const createPreview = (file: File): string => {
    const url = URL.createObjectURL(file);
    urlsRef.current.add(url);
    return url;
  };

  const cleanupPreview = (url: string) => {
    URL.revokeObjectURL(url);
    urlsRef.current.delete(url);
  };

  const cleanupAll = () => {
    urlsRef.current.forEach(url => URL.revokeObjectURL(url));
    urlsRef.current.clear();
  };

  useEffect(() => {
    return cleanupAll;
  }, []);

  return { createPreview, cleanupPreview, cleanupAll };
}
```