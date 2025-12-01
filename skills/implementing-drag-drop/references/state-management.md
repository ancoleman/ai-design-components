# State Management for Drag-and-Drop

## Table of Contents
- [React State Patterns](#react-state-patterns)
- [Optimistic Updates](#optimistic-updates)
- [Undo/Redo Functionality](#undoredo-functionality)
- [Persistence Strategies](#persistence-strategies)
- [Multi-User Synchronization](#multi-user-synchronization)
- [Error Recovery](#error-recovery)

## React State Patterns

### Basic Drag State Management

```tsx
interface DragState {
  isDragging: boolean;
  draggedItem: any | null;
  draggedFrom: string | null;
  draggedOver: string | null;
  initialPosition: { x: number; y: number } | null;
  currentPosition: { x: number; y: number } | null;
}

function useDragState() {
  const [dragState, setDragState] = useState<DragState>({
    isDragging: false,
    draggedItem: null,
    draggedFrom: null,
    draggedOver: null,
    initialPosition: null,
    currentPosition: null,
  });

  const startDrag = useCallback((item: any, from: string, position: { x: number; y: number }) => {
    setDragState({
      isDragging: true,
      draggedItem: item,
      draggedFrom: from,
      draggedOver: null,
      initialPosition: position,
      currentPosition: position,
    });
  }, []);

  const updateDrag = useCallback((over: string | null, position: { x: number; y: number }) => {
    setDragState(prev => ({
      ...prev,
      draggedOver: over,
      currentPosition: position,
    }));
  }, []);

  const endDrag = useCallback(() => {
    setDragState({
      isDragging: false,
      draggedItem: null,
      draggedFrom: null,
      draggedOver: null,
      initialPosition: null,
      currentPosition: null,
    });
  }, []);

  return {
    dragState,
    startDrag,
    updateDrag,
    endDrag,
  };
}
```

### Context-Based State Management

```tsx
// DragDropContext.tsx
interface DragDropContextValue {
  items: Record<string, Item[]>;
  moveItem: (item: Item, fromContainer: string, toContainer: string, toIndex: number) => void;
  reorderItems: (container: string, fromIndex: number, toIndex: number) => void;
  isDragging: boolean;
  draggedItem: Item | null;
  canDrop: (container: string) => boolean;
}

const DragDropContext = createContext<DragDropContextValue | null>(null);

export function DragDropProvider({ children, initialItems }) {
  const [items, setItems] = useState(initialItems);
  const [draggedItem, setDraggedItem] = useState<Item | null>(null);

  const moveItem = useCallback((
    item: Item,
    fromContainer: string,
    toContainer: string,
    toIndex: number
  ) => {
    setItems(prev => {
      const newItems = { ...prev };

      // Remove from source
      newItems[fromContainer] = newItems[fromContainer].filter(i => i.id !== item.id);

      // Add to destination
      newItems[toContainer] = [
        ...newItems[toContainer].slice(0, toIndex),
        item,
        ...newItems[toContainer].slice(toIndex),
      ];

      return newItems;
    });
  }, []);

  const reorderItems = useCallback((
    container: string,
    fromIndex: number,
    toIndex: number
  ) => {
    setItems(prev => {
      const newItems = { ...prev };
      const containerItems = [...newItems[container]];

      const [movedItem] = containerItems.splice(fromIndex, 1);
      containerItems.splice(toIndex, 0, movedItem);

      newItems[container] = containerItems;
      return newItems;
    });
  }, []);

  const canDrop = useCallback((container: string) => {
    // Custom drop rules
    const maxItems = 10;
    return items[container]?.length < maxItems;
  }, [items]);

  const value = useMemo(
    () => ({
      items,
      moveItem,
      reorderItems,
      isDragging: draggedItem !== null,
      draggedItem,
      canDrop,
    }),
    [items, moveItem, reorderItems, draggedItem, canDrop]
  );

  return (
    <DragDropContext.Provider value={value}>
      <DndContext
        onDragStart={(event) => setDraggedItem(event.active.data.current?.item)}
        onDragEnd={() => setDraggedItem(null)}
      >
        {children}
      </DndContext>
    </DragDropContext.Provider>
  );
}

export function useDragDrop() {
  const context = useContext(DragDropContext);
  if (!context) {
    throw new Error('useDragDrop must be used within DragDropProvider');
  }
  return context;
}
```

### Reducer Pattern for Complex State

```tsx
type DragAction =
  | { type: 'START_DRAG'; payload: { item: Item; source: string } }
  | { type: 'UPDATE_DRAG'; payload: { over: string; position: Position } }
  | { type: 'END_DRAG'; payload: { target: string; index: number } }
  | { type: 'CANCEL_DRAG' }
  | { type: 'REORDER'; payload: { container: string; from: number; to: number } }
  | { type: 'MOVE'; payload: { item: Item; from: string; to: string; index: number } };

interface DragDropState {
  containers: Record<string, Item[]>;
  dragState: {
    isDragging: boolean;
    item: Item | null;
    source: string | null;
    target: string | null;
  };
  history: DragDropState[];
  historyIndex: number;
}

function dragDropReducer(state: DragDropState, action: DragAction): DragDropState {
  switch (action.type) {
    case 'START_DRAG':
      return {
        ...state,
        dragState: {
          isDragging: true,
          item: action.payload.item,
          source: action.payload.source,
          target: null,
        },
      };

    case 'UPDATE_DRAG':
      return {
        ...state,
        dragState: {
          ...state.dragState,
          target: action.payload.over,
        },
      };

    case 'END_DRAG': {
      if (!state.dragState.item || !state.dragState.source) {
        return state;
      }

      const newContainers = { ...state.containers };
      const { item, source } = state.dragState;
      const { target, index } = action.payload;

      // Remove from source
      newContainers[source] = newContainers[source].filter(i => i.id !== item.id);

      // Add to target
      newContainers[target] = [
        ...newContainers[target].slice(0, index),
        item,
        ...newContainers[target].slice(index),
      ];

      // Add to history for undo
      const newState = {
        containers: newContainers,
        dragState: {
          isDragging: false,
          item: null,
          source: null,
          target: null,
        },
        history: [...state.history.slice(0, state.historyIndex + 1), state],
        historyIndex: state.historyIndex + 1,
      };

      return newState;
    }

    case 'CANCEL_DRAG':
      return {
        ...state,
        dragState: {
          isDragging: false,
          item: null,
          source: null,
          target: null,
        },
      };

    default:
      return state;
  }
}
```

## Optimistic Updates

### Optimistic UI Pattern

```tsx
interface OptimisticUpdate<T> {
  id: string;
  action: () => Promise<T>;
  optimistic: T;
  rollback: T;
  timestamp: number;
}

function useOptimisticUpdates<T>() {
  const [pending, setPending] = useState<Map<string, OptimisticUpdate<T>>>(new Map());
  const [failed, setFailed] = useState<Map<string, Error>>(new Map());

  const executeOptimistic = async (
    id: string,
    action: () => Promise<T>,
    optimistic: T,
    rollback: T
  ) => {
    // Apply optimistic update immediately
    setPending(prev => new Map(prev).set(id, {
      id,
      action,
      optimistic,
      rollback,
      timestamp: Date.now(),
    }));

    try {
      // Execute the actual action
      const result = await action();

      // Remove from pending on success
      setPending(prev => {
        const next = new Map(prev);
        next.delete(id);
        return next;
      });

      return result;
    } catch (error) {
      // Mark as failed and rollback
      setFailed(prev => new Map(prev).set(id, error as Error));

      // Apply rollback
      setPending(prev => {
        const next = new Map(prev);
        const update = next.get(id);
        if (update) {
          next.set(id, { ...update, optimistic: rollback });
        }
        return next;
      });

      throw error;
    }
  };

  const retry = async (id: string) => {
    const update = pending.get(id);
    if (!update) return;

    setFailed(prev => {
      const next = new Map(prev);
      next.delete(id);
      return next;
    });

    await executeOptimistic(id, update.action, update.optimistic, update.rollback);
  };

  return { pending, failed, executeOptimistic, retry };
}

// Usage in drag-drop
function OptimisticDragDrop({ items, onSave }) {
  const [localItems, setLocalItems] = useState(items);
  const { executeOptimistic, failed } = useOptimisticUpdates();

  const handleDragEnd = async (event) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    const oldItems = [...localItems];
    const newItems = reorderItems(localItems, active.id, over.id);

    // Apply optimistically
    setLocalItems(newItems);

    // Save to server with rollback
    await executeOptimistic(
      `reorder-${Date.now()}`,
      () => onSave(newItems),
      newItems,
      oldItems
    ).catch(() => {
      // Rollback handled automatically
      setLocalItems(oldItems);
      toast.error('Failed to save. Please try again.');
    });
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      {failed.size > 0 && (
        <div className="error-banner">
          Some changes failed to save. Retrying...
        </div>
      )}
      {/* Render items */}
    </DndContext>
  );
}
```

## Undo/Redo Functionality

### History Management

```tsx
interface HistoryState<T> {
  past: T[];
  present: T;
  future: T[];
}

function useHistory<T>(initialState: T) {
  const [history, setHistory] = useState<HistoryState<T>>({
    past: [],
    present: initialState,
    future: [],
  });

  const canUndo = history.past.length > 0;
  const canRedo = history.future.length > 0;

  const push = useCallback((newState: T) => {
    setHistory(prev => ({
      past: [...prev.past, prev.present],
      present: newState,
      future: [], // Clear future on new action
    }));
  }, []);

  const undo = useCallback(() => {
    setHistory(prev => {
      if (prev.past.length === 0) return prev;

      const previous = prev.past[prev.past.length - 1];
      const newPast = prev.past.slice(0, prev.past.length - 1);

      return {
        past: newPast,
        present: previous,
        future: [prev.present, ...prev.future],
      };
    });
  }, []);

  const redo = useCallback(() => {
    setHistory(prev => {
      if (prev.future.length === 0) return prev;

      const next = prev.future[0];
      const newFuture = prev.future.slice(1);

      return {
        past: [...prev.past, prev.present],
        present: next,
        future: newFuture,
      };
    });
  }, []);

  const reset = useCallback(() => {
    setHistory({
      past: [],
      present: initialState,
      future: [],
    });
  }, [initialState]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        if (canUndo) undo();
      }
      if ((e.metaKey || e.ctrlKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
        e.preventDefault();
        if (canRedo) redo();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [canUndo, canRedo, undo, redo]);

  return {
    state: history.present,
    push,
    undo,
    redo,
    reset,
    canUndo,
    canRedo,
    history,
  };
}

// Usage with drag-drop
function DragDropWithHistory() {
  const { state: items, push, undo, redo, canUndo, canRedo } = useHistory(initialItems);

  const handleDragEnd = (event) => {
    const newItems = reorderItems(items, event);
    push(newItems); // Save to history
  };

  return (
    <>
      <div className="controls">
        <button onClick={undo} disabled={!canUndo}>
          Undo (Ctrl+Z)
        </button>
        <button onClick={redo} disabled={!canRedo}>
          Redo (Ctrl+Y)
        </button>
      </div>

      <DndContext onDragEnd={handleDragEnd}>
        <SortableContext items={items}>
          {items.map(item => (
            <SortableItem key={item.id} item={item} />
          ))}
        </SortableContext>
      </DndContext>
    </>
  );
}
```

## Persistence Strategies

### Local Storage Persistence

```tsx
function useLocalStorageState<T>(key: string, defaultValue: T) {
  const [state, setState] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  });

  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    setState(prev => {
      const nextState = value instanceof Function ? value(prev) : value;

      try {
        localStorage.setItem(key, JSON.stringify(nextState));
      } catch (error) {
        console.error('Failed to save to localStorage:', error);
      }

      return nextState;
    });
  }, [key]);

  // Sync between tabs
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key && e.newValue) {
        try {
          setState(JSON.parse(e.newValue));
        } catch {}
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);

  return [state, setValue] as const;
}

// Auto-save with debouncing
function AutoSaveDragDrop() {
  const [items, setItems] = useLocalStorageState('drag-drop-items', initialItems);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const debouncedItems = useDebounce(items, 1000);

  useEffect(() => {
    if (debouncedItems !== items) {
      setLastSaved(new Date());
    }
  }, [debouncedItems]);

  return (
    <div>
      {lastSaved && (
        <div className="save-indicator">
          Last saved: {lastSaved.toLocaleTimeString()}
        </div>
      )}

      <DndContext onDragEnd={(event) => {
        const newItems = reorderItems(items, event);
        setItems(newItems);
      }}>
        {/* Content */}
      </DndContext>
    </div>
  );
}
```

### IndexedDB for Large Datasets

```tsx
class DragDropStore {
  private db: IDBDatabase | null = null;
  private dbName = 'DragDropDB';
  private storeName = 'items';

  async init() {
    return new Promise<void>((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' });
        }
      };

      request.onsuccess = (event) => {
        this.db = (event.target as IDBOpenDBRequest).result;
        resolve();
      };

      request.onerror = () => reject(request.error);
    });
  }

  async saveItems(items: Item[]) {
    if (!this.db) await this.init();

    const transaction = this.db!.transaction([this.storeName], 'readwrite');
    const store = transaction.objectStore(this.storeName);

    // Clear existing items
    await new Promise((resolve, reject) => {
      const clearRequest = store.clear();
      clearRequest.onsuccess = () => resolve(true);
      clearRequest.onerror = () => reject(clearRequest.error);
    });

    // Add new items
    for (const item of items) {
      store.add(item);
    }

    return new Promise<void>((resolve, reject) => {
      transaction.oncomplete = () => resolve();
      transaction.onerror = () => reject(transaction.error);
    });
  }

  async loadItems(): Promise<Item[]> {
    if (!this.db) await this.init();

    const transaction = this.db!.transaction([this.storeName], 'readonly');
    const store = transaction.objectStore(this.storeName);

    return new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
}

// Hook for IndexedDB persistence
function useIndexedDBState(initialItems: Item[]) {
  const [items, setItems] = useState(initialItems);
  const [loading, setLoading] = useState(true);
  const store = useRef(new DragDropStore());

  // Load from IndexedDB on mount
  useEffect(() => {
    store.current.loadItems()
      .then(savedItems => {
        if (savedItems.length > 0) {
          setItems(savedItems);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  // Save to IndexedDB on change
  const saveItems = useCallback(async (newItems: Item[]) => {
    setItems(newItems);
    await store.current.saveItems(newItems);
  }, []);

  return { items, saveItems, loading };
}
```

## Multi-User Synchronization

### WebSocket Real-Time Sync

```tsx
function useRealtimeDragDrop(roomId: string) {
  const [items, setItems] = useState<Item[]>([]);
  const [otherUsers, setOtherUsers] = useState<Map<string, UserCursor>>(new Map());
  const ws = useRef<WebSocket>();

  useEffect(() => {
    ws.current = new WebSocket(`wss://api.example.com/rooms/${roomId}`);

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case 'ITEMS_UPDATE':
          setItems(message.items);
          break;

        case 'USER_DRAGGING':
          setOtherUsers(prev => new Map(prev).set(message.userId, {
            item: message.item,
            position: message.position,
            color: message.color,
          }));
          break;

        case 'USER_DROPPED':
          setOtherUsers(prev => {
            const next = new Map(prev);
            next.delete(message.userId);
            return next;
          });
          break;
      }
    };

    return () => ws.current?.close();
  }, [roomId]);

  const handleDragStart = (event) => {
    ws.current?.send(JSON.stringify({
      type: 'DRAG_START',
      item: event.active.data.current?.item,
      position: { x: event.active.rect.current.translated.left, y: event.active.rect.current.translated.top },
    }));
  };

  const handleDragEnd = (event) => {
    const newItems = reorderItems(items, event);

    // Optimistic update
    setItems(newItems);

    // Broadcast change
    ws.current?.send(JSON.stringify({
      type: 'DRAG_END',
      items: newItems,
    }));
  };

  return {
    items,
    otherUsers,
    handleDragStart,
    handleDragEnd,
  };
}
```

## Error Recovery

### Error Boundary for Drag-Drop

```tsx
class DragDropErrorBoundary extends Component<
  { children: React.ReactNode; onError?: (error: Error) => void },
  { hasError: boolean; error: Error | null }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Drag-drop error:', error, errorInfo);
    this.props.onError?.(error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong with drag-and-drop</h2>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Reset
          </button>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.stack}</pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

// Wrap drag-drop components
function SafeDragDrop({ children }) {
  return (
    <DragDropErrorBoundary
      onError={(error) => {
        // Log to error tracking service
        logError(error, { context: 'drag-drop' });
      }}
    >
      {children}
    </DragDropErrorBoundary>
  );
}
```