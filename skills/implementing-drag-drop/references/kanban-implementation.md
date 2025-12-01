# Kanban Board Implementation

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Multi-Container Dragging](#multi-container-dragging)
- [Card Management](#card-management)
- [Column Features](#column-features)
- [Advanced Features](#advanced-features)
- [Performance Optimization](#performance-optimization)

## Architecture Overview

### Data Structure

```typescript
// types/kanban.ts
export interface KanbanCard {
  id: string;
  title: string;
  description?: string;
  assignee?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  tags?: string[];
  createdAt: Date;
  updatedAt: Date;
  columnId: string;
  order: number;
}

export interface KanbanColumn {
  id: string;
  title: string;
  order: number;
  wipLimit?: number;
  collapsed?: boolean;
  color?: string;
}

export interface KanbanBoard {
  id: string;
  name: string;
  columns: KanbanColumn[];
  cards: KanbanCard[];
}

export interface DragData {
  type: 'card' | 'column';
  card?: KanbanCard;
  column?: KanbanColumn;
  fromColumnId?: string;
}
```

## Multi-Container Dragging

### Setup with dnd-kit

```tsx
import {
  DndContext,
  DragOverlay,
  closestCorners,
  pointerWithin,
  useSensor,
  useSensors,
  PointerSensor,
  KeyboardSensor,
} from '@dnd-kit/core';
import {
  SortableContext,
  arrayMove,
  verticalListSortingStrategy,
  horizontalListSortingStrategy,
} from '@dnd-kit/sortable';

function KanbanBoard({ board, onUpdate }) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [activeType, setActiveType] = useState<'card' | 'column' | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 10, // Prevent accidental drags
      },
    }),
    useSensor(KeyboardSensor)
  );

  // Group cards by column
  const cardsByColumn = useMemo(() => {
    const map = new Map<string, KanbanCard[]>();
    board.columns.forEach(col => {
      map.set(
        col.id,
        board.cards
          .filter(card => card.columnId === col.id)
          .sort((a, b) => a.order - b.order)
      );
    });
    return map;
  }, [board]);

  function handleDragStart(event) {
    const { active } = event;
    const type = active.data.current?.type;

    setActiveId(active.id);
    setActiveType(type);
  }

  function handleDragOver(event) {
    const { active, over } = event;

    if (!over) return;

    const activeType = active.data.current?.type;
    const overType = over.data.current?.type;

    // Card over column
    if (activeType === 'card' && overType === 'column') {
      const activeCard = board.cards.find(c => c.id === active.id);
      const overColumnId = over.id;

      if (activeCard && activeCard.columnId !== overColumnId) {
        // Move card to new column
        onUpdate({
          ...board,
          cards: board.cards.map(card =>
            card.id === activeCard.id
              ? { ...card, columnId: overColumnId }
              : card
          ),
        });
      }
    }

    // Card over card (reordering within or between columns)
    if (activeType === 'card' && overType === 'card') {
      const activeCard = board.cards.find(c => c.id === active.id);
      const overCard = board.cards.find(c => c.id === over.id);

      if (activeCard && overCard && activeCard.id !== overCard.id) {
        const activeColumnId = activeCard.columnId;
        const overColumnId = overCard.columnId;

        if (activeColumnId === overColumnId) {
          // Reorder within same column
          const columnCards = cardsByColumn.get(activeColumnId) || [];
          const oldIndex = columnCards.findIndex(c => c.id === active.id);
          const newIndex = columnCards.findIndex(c => c.id === over.id);

          if (oldIndex !== newIndex) {
            const reordered = arrayMove(columnCards, oldIndex, newIndex);
            updateCardOrder(activeColumnId, reordered);
          }
        } else {
          // Move between columns
          moveCardBetweenColumns(activeCard, overCard);
        }
      }
    }
  }

  function handleDragEnd(event) {
    const { active, over } = event;

    if (!over) {
      setActiveId(null);
      setActiveType(null);
      return;
    }

    // Handle column reordering
    if (activeType === 'column' && over.data.current?.type === 'column') {
      const oldIndex = board.columns.findIndex(c => c.id === active.id);
      const newIndex = board.columns.findIndex(c => c.id === over.id);

      if (oldIndex !== newIndex) {
        onUpdate({
          ...board,
          columns: arrayMove(board.columns, oldIndex, newIndex).map(
            (col, index) => ({ ...col, order: index })
          ),
        });
      }
    }

    setActiveId(null);
    setActiveType(null);
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
    >
      {/* Column sorting context */}
      <SortableContext
        items={board.columns.map(c => c.id)}
        strategy={horizontalListSortingStrategy}
      >
        <div className="kanban-board">
          {board.columns.map(column => (
            <KanbanColumn
              key={column.id}
              column={column}
              cards={cardsByColumn.get(column.id) || []}
            />
          ))}
        </div>
      </SortableContext>

      {/* Drag overlay for visual feedback */}
      <DragOverlay>
        {activeId && activeType === 'card' && (
          <CardDragPreview card={board.cards.find(c => c.id === activeId)} />
        )}
        {activeId && activeType === 'column' && (
          <ColumnDragPreview column={board.columns.find(c => c.id === activeId)} />
        )}
      </DragOverlay>
    </DndContext>
  );
}
```

## Card Management

### Sortable Cards within Columns

```tsx
function KanbanColumn({ column, cards }) {
  const {
    setNodeRef,
    attributes,
    listeners,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: column.id,
    data: { type: 'column', column },
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="kanban-column"
    >
      {/* Column header with drag handle */}
      <div className="column-header">
        <button
          className="drag-handle"
          {...attributes}
          {...listeners}
          aria-label={`Drag to reorder ${column.title} column`}
        >
          ⋮⋮
        </button>
        <h3>{column.title}</h3>
        <span className="card-count">{cards.length}</span>
        {column.wipLimit && (
          <span className={cards.length > column.wipLimit ? 'wip-exceeded' : 'wip-limit'}>
            {cards.length}/{column.wipLimit}
          </span>
        )}
      </div>

      {/* Cards container */}
      <SortableContext
        items={cards.map(c => c.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="cards-container">
          {cards.map(card => (
            <KanbanCard key={card.id} card={card} />
          ))}

          {/* Drop zone for empty columns */}
          {cards.length === 0 && (
            <div className="empty-column-drop-zone">
              Drop cards here
            </div>
          )}
        </div>
      </SortableContext>

      {/* Add card button */}
      <button className="add-card-btn">+ Add Card</button>
    </div>
  );
}
```

### Draggable Card Component

```tsx
function KanbanCard({ card }) {
  const {
    setNodeRef,
    attributes,
    listeners,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: card.id,
    data: { type: 'card', card },
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    cursor: isDragging ? 'grabbing' : 'grab',
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`kanban-card priority-${card.priority}`}
      {...attributes}
      {...listeners}
    >
      {/* Priority indicator */}
      {card.priority && (
        <div className={`priority-indicator priority-${card.priority}`} />
      )}

      {/* Card content */}
      <h4>{card.title}</h4>
      {card.description && (
        <p className="card-description">{card.description}</p>
      )}

      {/* Card metadata */}
      <div className="card-footer">
        {card.assignee && (
          <div className="assignee">
            <img src={`/avatars/${card.assignee}.png`} alt={card.assignee} />
          </div>
        )}
        {card.tags && (
          <div className="tags">
            {card.tags.map(tag => (
              <span key={tag} className="tag">{tag}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

## Column Features

### WIP Limits

```tsx
function enforceWipLimit(column: KanbanColumn, cards: KanbanCard[]): boolean {
  if (!column.wipLimit) return true;

  const currentCards = cards.filter(c => c.columnId === column.id);
  return currentCards.length < column.wipLimit;
}

// In drag handler
function handleDragOver(event) {
  const { active, over } = event;

  if (over?.data.current?.type === 'column') {
    const targetColumn = board.columns.find(c => c.id === over.id);

    if (!enforceWipLimit(targetColumn, board.cards)) {
      // Show visual feedback for WIP limit exceeded
      event.preventDefault();
      showNotification(`WIP limit (${targetColumn.wipLimit}) exceeded for ${targetColumn.title}`);
      return;
    }
  }
  // Continue with normal drag logic
}
```

### Collapsible Columns

```tsx
function CollapsibleColumn({ column, cards, onToggle }) {
  const [collapsed, setCollapsed] = useState(column.collapsed || false);

  const handleToggle = () => {
    setCollapsed(!collapsed);
    onToggle(column.id, !collapsed);
  };

  return (
    <div className={`kanban-column ${collapsed ? 'collapsed' : ''}`}>
      <div className="column-header">
        <button
          onClick={handleToggle}
          aria-expanded={!collapsed}
          aria-label={`${collapsed ? 'Expand' : 'Collapse'} ${column.title}`}
        >
          {collapsed ? '▶' : '▼'}
        </button>
        <h3>{column.title}</h3>
        <span className="card-count">{cards.length}</span>
      </div>

      {!collapsed && (
        <div className="cards-container">
          {/* Cards */}
        </div>
      )}

      {collapsed && (
        <div className="collapsed-indicator">
          {cards.length} card{cards.length !== 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
}
```

### Swimlanes

```tsx
interface Swimlane {
  id: string;
  title: string;
  order: number;
}

function KanbanBoardWithSwimlanes({ board, swimlanes }) {
  const cardsBySwimlane = useMemo(() => {
    const map = new Map<string, KanbanCard[]>();
    swimlanes.forEach(swimlane => {
      map.set(
        swimlane.id,
        board.cards.filter(card => card.swimlaneId === swimlane.id)
      );
    });
    return map;
  }, [board.cards, swimlanes]);

  return (
    <div className="kanban-board-swimlanes">
      {swimlanes.map(swimlane => (
        <div key={swimlane.id} className="swimlane">
          <div className="swimlane-header">
            <h3>{swimlane.title}</h3>
          </div>
          <div className="swimlane-columns">
            {board.columns.map(column => (
              <KanbanColumn
                key={`${swimlane.id}-${column.id}`}
                column={column}
                cards={cardsBySwimlane.get(swimlane.id)?.filter(
                  c => c.columnId === column.id
                ) || []}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## Advanced Features

### Card Preview on Hover

```tsx
function CardWithPreview({ card }) {
  const [showPreview, setShowPreview] = useState(false);
  const [previewPosition, setPreviewPosition] = useState({ x: 0, y: 0 });

  const handleMouseEnter = (e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setPreviewPosition({
      x: rect.right + 10,
      y: rect.top,
    });
    setShowPreview(true);
  };

  return (
    <>
      <div
        onMouseEnter={handleMouseEnter}
        onMouseLeave={() => setShowPreview(false)}
        className="kanban-card"
      >
        {/* Card content */}
      </div>

      {showPreview && (
        <div
          className="card-preview"
          style={{
            position: 'fixed',
            left: previewPosition.x,
            top: previewPosition.y,
            zIndex: 1000,
          }}
        >
          <h4>{card.title}</h4>
          <p>{card.description}</p>
          <div className="preview-metadata">
            <span>Created: {formatDate(card.createdAt)}</span>
            <span>Updated: {formatDate(card.updatedAt)}</span>
            {card.dueDate && (
              <span className="due-date">Due: {formatDate(card.dueDate)}</span>
            )}
          </div>
          {card.comments && (
            <div className="preview-comments">
              {card.comments.length} comment(s)
            </div>
          )}
        </div>
      )}
    </>
  );
}
```

### Auto-Scroll on Drag

```tsx
function ScrollableKanbanBoard({ board }) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    if (!isDragging || !scrollContainerRef.current) return;

    const container = scrollContainerRef.current;
    let scrollInterval: NodeJS.Timeout;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const scrollThreshold = 50; // pixels from edge
      const scrollSpeed = 10; // pixels per frame

      clearInterval(scrollInterval);

      // Horizontal scrolling
      if (e.clientX < rect.left + scrollThreshold) {
        scrollInterval = setInterval(() => {
          container.scrollLeft -= scrollSpeed;
        }, 16); // ~60fps
      } else if (e.clientX > rect.right - scrollThreshold) {
        scrollInterval = setInterval(() => {
          container.scrollLeft += scrollSpeed;
        }, 16);
      }

      // Vertical scrolling
      if (e.clientY < rect.top + scrollThreshold) {
        scrollInterval = setInterval(() => {
          container.scrollTop -= scrollSpeed;
        }, 16);
      } else if (e.clientY > rect.bottom - scrollThreshold) {
        scrollInterval = setInterval(() => {
          container.scrollTop += scrollSpeed;
        }, 16);
      }
    };

    document.addEventListener('mousemove', handleMouseMove);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      clearInterval(scrollInterval);
    };
  }, [isDragging]);

  return (
    <div ref={scrollContainerRef} className="kanban-scroll-container">
      <DndContext
        onDragStart={() => setIsDragging(true)}
        onDragEnd={() => setIsDragging(false)}
      >
        {/* Board content */}
      </DndContext>
    </div>
  );
}
```

### Column Management

```tsx
function ColumnManager({ columns, onUpdate }) {
  const [newColumnName, setNewColumnName] = useState('');
  const [showAddColumn, setShowAddColumn] = useState(false);

  const handleAddColumn = () => {
    if (!newColumnName.trim()) return;

    const newColumn: KanbanColumn = {
      id: generateId(),
      title: newColumnName,
      order: columns.length,
      wipLimit: undefined,
      collapsed: false,
    };

    onUpdate([...columns, newColumn]);
    setNewColumnName('');
    setShowAddColumn(false);
  };

  const handleDeleteColumn = (columnId: string) => {
    if (confirm('Delete this column? All cards will be moved to backlog.')) {
      onUpdate(columns.filter(c => c.id !== columnId));
    }
  };

  const handleRenameColumn = (columnId: string, newName: string) => {
    onUpdate(
      columns.map(c =>
        c.id === columnId ? { ...c, title: newName } : c
      )
    );
  };

  return (
    <div className="column-manager">
      {/* Add column button/form */}
      {showAddColumn ? (
        <div className="add-column-form">
          <input
            type="text"
            value={newColumnName}
            onChange={(e) => setNewColumnName(e.target.value)}
            placeholder="Column name"
            autoFocus
          />
          <button onClick={handleAddColumn}>Add</button>
          <button onClick={() => setShowAddColumn(false)}>Cancel</button>
        </div>
      ) : (
        <button onClick={() => setShowAddColumn(true)}>
          + Add Column
        </button>
      )}

      {/* Column settings */}
      {columns.map(column => (
        <ColumnSettings
          key={column.id}
          column={column}
          onRename={handleRenameColumn}
          onDelete={handleDeleteColumn}
        />
      ))}
    </div>
  );
}
```

## Performance Optimization

### Virtual Scrolling for Large Boards

```tsx
import { FixedSizeList } from 'react-window';

function VirtualizedColumn({ column, cards, height }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <KanbanCard card={cards[index]} />
    </div>
  );

  return (
    <div className="kanban-column">
      <div className="column-header">
        <h3>{column.title}</h3>
      </div>

      <FixedSizeList
        height={height}
        itemCount={cards.length}
        itemSize={120} // Average card height
        width="100%"
      >
        {Row}
      </FixedSizeList>
    </div>
  );
}
```

### Optimistic Updates

```tsx
function useOptimisticKanban(initialBoard: KanbanBoard) {
  const [board, setBoard] = useState(initialBoard);
  const [pendingUpdates, setPendingUpdates] = useState<Map<string, any>>(new Map());

  const updateBoard = async (newBoard: KanbanBoard) => {
    const updateId = generateId();

    // Optimistic update
    setBoard(newBoard);
    setPendingUpdates(prev => new Map(prev).set(updateId, newBoard));

    try {
      // Persist to server
      await api.updateBoard(newBoard);

      // Remove from pending
      setPendingUpdates(prev => {
        const next = new Map(prev);
        next.delete(updateId);
        return next;
      });
    } catch (error) {
      // Rollback on error
      setBoard(initialBoard);
      setPendingUpdates(new Map());
      console.error('Failed to update board:', error);
      showNotification('Failed to save changes. Please try again.');
    }
  };

  return { board, updateBoard, isPending: pendingUpdates.size > 0 };
}
```

### Memoization

```tsx
const MemoizedKanbanCard = memo(KanbanCard, (prev, next) => {
  return (
    prev.card.id === next.card.id &&
    prev.card.title === next.card.title &&
    prev.card.description === next.card.description &&
    prev.card.columnId === next.card.columnId &&
    prev.card.order === next.card.order
  );
});

const MemoizedColumn = memo(KanbanColumn, (prev, next) => {
  return (
    prev.column.id === next.column.id &&
    prev.column.title === next.column.title &&
    prev.cards.length === next.cards.length &&
    prev.cards.every((card, index) => card.id === next.cards[index]?.id)
  );
});
```