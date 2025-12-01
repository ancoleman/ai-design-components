import React, { useState, useMemo } from 'react';
import {
  DndContext,
  DragOverlay,
  closestCorners,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragStartEvent,
  DragOverEvent,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  horizontalListSortingStrategy,
} from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

// Types
interface Task {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assignee?: string;
  tags: string[];
  columnId: string;
}

interface Column {
  id: string;
  title: string;
  wipLimit?: number;
  color: string;
}

// Draggable Task Card
function TaskCard({ task, isDragging }: { task: Task; isDragging?: boolean }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({
    id: task.id,
    data: {
      type: 'task',
      task,
    },
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
      className={`task-card priority-${task.priority}`}
      {...attributes}
      {...listeners}
    >
      <div className="task-header">
        <h4 className="task-title">{task.title}</h4>
        <span className={`priority-indicator priority-${task.priority}`} />
      </div>

      <p className="task-description">{task.description}</p>

      <div className="task-footer">
        {task.assignee && (
          <div className="assignee">
            <img
              src={`https://ui-avatars.com/api/?name=${task.assignee}&size=24`}
              alt={task.assignee}
              title={task.assignee}
            />
          </div>
        )}

        <div className="tags">
          {task.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

// Droppable Column
function BoardColumn({
  column,
  tasks,
  isOver,
}: {
  column: Column;
  tasks: Task[];
  isOver?: boolean;
}) {
  const {
    setNodeRef,
    attributes,
    listeners,
    transform,
    transition,
  } = useSortable({
    id: column.id,
    data: {
      type: 'column',
      column,
    },
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const isOverLimit = column.wipLimit && tasks.length >= column.wipLimit;

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`board-column ${isOver ? 'column-over' : ''} ${
        isOverLimit ? 'over-limit' : ''
      }`}
    >
      <div
        className="column-header"
        style={{ borderTopColor: column.color }}
      >
        <button
          className="column-drag-handle"
          {...attributes}
          {...listeners}
          aria-label={`Drag to reorder ${column.title} column`}
        >
          ⋮⋮
        </button>

        <h3 className="column-title">{column.title}</h3>

        <span className="task-count">
          {tasks.length}
          {column.wipLimit && ` / ${column.wipLimit}`}
        </span>
      </div>

      <SortableContext
        items={tasks.map((t) => t.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="tasks-container">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}

          {tasks.length === 0 && (
            <div className="empty-column">
              Drop tasks here
            </div>
          )}
        </div>
      </SortableContext>

      <button className="add-task-btn">
        + Add Task
      </button>
    </div>
  );
}

// Main Kanban Board
export function KanbanBoard() {
  const [columns] = useState<Column[]>([
    { id: 'backlog', title: 'Backlog', color: '#94a3b8' },
    { id: 'todo', title: 'To Do', color: '#60a5fa', wipLimit: 5 },
    { id: 'inprogress', title: 'In Progress', color: '#fbbf24', wipLimit: 3 },
    { id: 'review', title: 'Review', color: '#a78bfa', wipLimit: 2 },
    { id: 'done', title: 'Done', color: '#34d399' },
  ]);

  const [tasks, setTasks] = useState<Task[]>([
    {
      id: 'task-1',
      title: 'Setup project repository',
      description: 'Initialize git repo and add initial files',
      priority: 'high',
      assignee: 'John Doe',
      tags: ['setup', 'git'],
      columnId: 'done',
    },
    {
      id: 'task-2',
      title: 'Design database schema',
      description: 'Create ERD and define relationships',
      priority: 'urgent',
      assignee: 'Jane Smith',
      tags: ['backend', 'database'],
      columnId: 'inprogress',
    },
    {
      id: 'task-3',
      title: 'Implement authentication',
      description: 'Add JWT-based auth system',
      priority: 'high',
      assignee: 'John Doe',
      tags: ['backend', 'security'],
      columnId: 'todo',
    },
    {
      id: 'task-4',
      title: 'Create landing page',
      description: 'Design and implement homepage',
      priority: 'medium',
      tags: ['frontend', 'design'],
      columnId: 'todo',
    },
    {
      id: 'task-5',
      title: 'Write API documentation',
      description: 'Document all API endpoints',
      priority: 'low',
      tags: ['documentation'],
      columnId: 'backlog',
    },
  ]);

  const [activeId, setActiveId] = useState<string | null>(null);

  // Group tasks by column
  const tasksByColumn = useMemo(() => {
    const map: Record<string, Task[]> = {};
    columns.forEach((col) => {
      map[col.id] = tasks.filter((task) => task.columnId === col.id);
    });
    return map;
  }, [tasks, columns]);

  // Sensors for drag detection
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

  // Find container for task
  function findContainer(id: string) {
    if (columns.find((col) => col.id === id)) {
      return id;
    }
    const task = tasks.find((t) => t.id === id);
    return task?.columnId;
  }

  // Drag handlers
  function handleDragStart(event: DragStartEvent) {
    const { active } = event;
    setActiveId(active.id as string);
  }

  function handleDragOver(event: DragOverEvent) {
    const { active, over } = event;
    if (!over) return;

    const activeContainer = findContainer(active.id as string);
    const overContainer = findContainer(over.id as string);

    if (!activeContainer || !overContainer || activeContainer === overContainer) {
      return;
    }

    setTasks((prev) => {
      const activeTask = prev.find((t) => t.id === active.id);
      if (!activeTask) return prev;

      // Check WIP limit
      const overColumn = columns.find((c) => c.id === overContainer);
      if (overColumn?.wipLimit) {
        const tasksInColumn = prev.filter((t) => t.columnId === overContainer);
        if (tasksInColumn.length >= overColumn.wipLimit) {
          // Show warning
          console.warn(`Column ${overColumn.title} has reached its WIP limit`);
          return prev;
        }
      }

      // Move task to new column
      return prev.map((task) =>
        task.id === activeTask.id
          ? { ...task, columnId: overContainer }
          : task
      );
    });
  }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (!over) {
      setActiveId(null);
      return;
    }

    const activeContainer = findContainer(active.id as string);
    const overContainer = findContainer(over.id as string);

    if (!activeContainer || !overContainer) {
      setActiveId(null);
      return;
    }

    if (activeContainer === overContainer) {
      // Reorder within same column
      const containerTasks = tasksByColumn[overContainer];
      const oldIndex = containerTasks.findIndex((t) => t.id === active.id);
      const newIndex = containerTasks.findIndex((t) => t.id === over.id);

      if (oldIndex !== newIndex) {
        const newTasks = arrayMove(containerTasks, oldIndex, newIndex);
        setTasks((prev) => [
          ...prev.filter((t) => t.columnId !== overContainer),
          ...newTasks,
        ]);
      }
    }

    setActiveId(null);
  }

  const activeTask = activeId ? tasks.find((t) => t.id === activeId) : null;

  return (
    <div className="kanban-board">
      <h2>Project Board</h2>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCorners}
        onDragStart={handleDragStart}
        onDragOver={handleDragOver}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={columns.map((c) => c.id)}
          strategy={horizontalListSortingStrategy}
        >
          <div className="columns-container">
            {columns.map((column) => (
              <BoardColumn
                key={column.id}
                column={column}
                tasks={tasksByColumn[column.id] || []}
              />
            ))}
          </div>
        </SortableContext>

        <DragOverlay>
          {activeTask && <TaskCard task={activeTask} isDragging />}
        </DragOverlay>
      </DndContext>
    </div>
  );
}

// Styles
const styles = `
.kanban-board {
  padding: 2rem;
  background: var(--color-gray-50);
  min-height: 100vh;
}

.columns-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 2rem;
}

.board-column {
  flex: 0 0 320px;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 120px);
}

.board-column.column-over {
  background: var(--color-primary-50);
  box-shadow: var(--shadow-md);
}

.board-column.over-limit {
  background: var(--color-red-50);
}

.column-header {
  padding: 1rem;
  border-top: 3px solid;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.column-drag-handle {
  cursor: grab;
  padding: 0.25rem;
  background: transparent;
  border: none;
  color: var(--color-text-tertiary);
}

.column-title {
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.task-count {
  background: var(--color-gray-100);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 500;
}

.tasks-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.task-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1rem;
  cursor: grab;
  transition: all 0.2s;
}

.task-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.task-card.priority-urgent {
  border-left: 3px solid var(--color-red-500);
}

.task-card.priority-high {
  border-left: 3px solid var(--color-orange-500);
}

.task-card.priority-medium {
  border-left: 3px solid var(--color-yellow-500);
}

.task-card.priority-low {
  border-left: 3px solid var(--color-blue-500);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 0.5rem;
}

.task-title {
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.priority-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.priority-indicator.priority-urgent {
  background: var(--color-red-500);
}

.priority-indicator.priority-high {
  background: var(--color-orange-500);
}

.priority-indicator.priority-medium {
  background: var(--color-yellow-500);
}

.priority-indicator.priority-low {
  background: var(--color-blue-500);
}

.task-description {
  font-size: 0.813rem;
  color: var(--color-text-secondary);
  margin: 0.5rem 0;
  line-height: 1.4;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.75rem;
}

.assignee img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--color-white);
}

.tags {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.tag {
  background: var(--color-gray-100);
  color: var(--color-text-secondary);
  padding: 0.125rem 0.375rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
}

.empty-column {
  padding: 2rem;
  text-align: center;
  color: var(--color-text-tertiary);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  margin: 0.5rem;
}

.add-task-btn {
  margin: 0.5rem;
  padding: 0.75rem;
  background: transparent;
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.add-task-btn:hover {
  background: var(--color-gray-50);
  border-color: var(--color-primary);
  color: var(--color-primary);
}
`;