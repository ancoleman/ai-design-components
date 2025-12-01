/**
 * TypeScript Types for Drag-and-Drop State Management
 */

import type { Active, Over, DragStartEvent, DragEndEvent, DragOverEvent, DragCancelEvent } from '@dnd-kit/core';

// Basic drag state
export interface DragState {
  isDragging: boolean;
  draggedItem: DraggableItem | null;
  draggedFrom: string | null;
  draggedOver: string | null;
  initialPosition: Position | null;
  currentPosition: Position | null;
}

// Position coordinates
export interface Position {
  x: number;
  y: number;
}

// Draggable item interface
export interface DraggableItem {
  id: string;
  content: React.ReactNode;
  order?: number;
  parentId?: string;
  type?: string;
  data?: Record<string, any>;
}

// Container interface for multi-container drag-drop
export interface DroppableContainer {
  id: string;
  title: string;
  items: DraggableItem[];
  acceptTypes?: string[];
  maxItems?: number;
  disabled?: boolean;
}

// Event handlers
export interface DragEventHandlers {
  onDragStart?: (event: DragStartEvent) => void;
  onDragMove?: (event: DragOverEvent) => void;
  onDragOver?: (event: DragOverEvent) => void;
  onDragEnd?: (event: DragEndEvent) => void;
  onDragCancel?: (event: DragCancelEvent) => void;
}

// Sensor configuration
export interface SensorConfig {
  pointer?: {
    enabled: boolean;
    activationConstraint?: {
      distance?: number;
      delay?: number;
      tolerance?: number;
    };
  };
  keyboard?: {
    enabled: boolean;
    coordinateGetter?: string;
    scrollBehavior?: 'auto' | 'smooth';
  };
  touch?: {
    enabled: boolean;
    activationConstraint?: {
      delay?: number;
      tolerance?: number;
    };
  };
}

// Animation configuration
export interface AnimationConfig {
  duration?: number;
  easing?: string;
  dragOverlay?: {
    opacity?: number;
    scale?: number;
  };
  dropAnimation?: {
    duration?: number;
    easing?: string;
    keyframes?: Keyframe[];
  };
}

// Collision detection strategies
export type CollisionDetectionStrategy =
  | 'closestCenter'
  | 'closestCorners'
  | 'rectIntersection'
  | 'pointerWithin'
  | ((args: any) => any);

// Sorting strategies
export type SortingStrategy =
  | 'vertical'
  | 'horizontal'
  | 'grid'
  | 'rect';

// Accessibility configuration
export interface AccessibilityConfig {
  announcements?: {
    onDragStart?: (id: string) => string;
    onDragOver?: (activeId: string, overId?: string) => string;
    onDragEnd?: (activeId: string, overId?: string) => string;
    onDragCancel?: (id: string) => string;
  };
  screenReaderInstructions?: string;
  ariaDescribedBy?: string;
  liveRegion?: boolean;
}

// Auto-scroll configuration
export interface AutoScrollConfig {
  enabled?: boolean;
  threshold?: {
    x?: number;
    y?: number;
  };
  maxSpeed?: number;
  acceleration?: number;
  interval?: number;
  canScroll?: (element: Element) => boolean;
}

// Complete dnd-kit configuration
export interface DndKitConfig {
  sensors?: SensorConfig;
  collisionDetection?: CollisionDetectionStrategy;
  sortingStrategy?: SortingStrategy;
  animation?: AnimationConfig;
  accessibility?: AccessibilityConfig;
  autoScroll?: AutoScrollConfig;
  modifiers?: Array<(args: any) => any>;
}

// Kanban-specific types
export namespace Kanban {
  export interface Task {
    id: string;
    title: string;
    description?: string;
    columnId: string;
    order: number;
    priority?: 'low' | 'medium' | 'high' | 'urgent';
    assignee?: string;
    tags?: string[];
    dueDate?: Date;
    createdAt: Date;
    updatedAt: Date;
  }

  export interface Column {
    id: string;
    title: string;
    order: number;
    wipLimit?: number;
    collapsed?: boolean;
    color?: string;
  }

  export interface Board {
    id: string;
    name: string;
    columns: Column[];
    tasks: Task[];
  }

  export interface Swimlane {
    id: string;
    title: string;
    order: number;
    collapsed?: boolean;
  }
}

// File upload types
export namespace FileUpload {
  export interface FileWithMeta extends File {
    id: string;
    preview?: string;
    progress: number;
    status: 'pending' | 'uploading' | 'success' | 'error';
    error?: string;
  }

  export interface DropzoneConfig {
    accept?: Record<string, string[]>;
    maxSize?: number;
    minSize?: number;
    maxFiles?: number;
    multiple?: boolean;
    disabled?: boolean;
    validator?: (file: File) => boolean | Promise<boolean>;
  }

  export interface UploadProgress {
    loaded: number;
    total: number;
    percentage: number;
  }
}

// Grid layout types
export namespace Grid {
  export interface GridItem {
    id: string;
    x: number;
    y: number;
    width: number;
    height: number;
    minWidth?: number;
    maxWidth?: number;
    minHeight?: number;
    maxHeight?: number;
    isDraggable?: boolean;
    isResizable?: boolean;
    static?: boolean;
  }

  export interface GridLayout {
    columns: number;
    rowHeight: number;
    width: number;
    margin?: [number, number];
    containerPadding?: [number, number];
    isDragging?: boolean;
    isResizing?: boolean;
  }
}

// History/Undo types
export interface HistoryState<T> {
  past: T[];
  present: T;
  future: T[];
}

export interface UndoableAction<T> {
  type: string;
  payload: T;
  timestamp: number;
  undo: () => void;
  redo: () => void;
}

// Multi-user sync types
export namespace Sync {
  export interface UserCursor {
    userId: string;
    userName: string;
    color: string;
    position: Position;
    draggedItem?: DraggableItem;
  }

  export interface SyncMessage {
    type: 'DRAG_START' | 'DRAG_MOVE' | 'DRAG_END' | 'STATE_UPDATE';
    userId: string;
    timestamp: number;
    data: any;
  }

  export interface CollaborationState {
    users: Map<string, UserCursor>;
    localUserId: string;
    isConnected: boolean;
  }
}

// Utility types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> =
  Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>;
  }[Keys];

// Hook return types
export interface UseDragDropReturn {
  isDragging: boolean;
  activeId: string | null;
  overId: string | null;
  handleDragStart: (event: DragStartEvent) => void;
  handleDragOver: (event: DragOverEvent) => void;
  handleDragEnd: (event: DragEndEvent) => void;
  handleDragCancel: (event: DragCancelEvent) => void;
}

export interface UseDroppableReturn {
  isOver: boolean;
  setNodeRef: (element: HTMLElement | null) => void;
  active: Active | null;
  over: Over | null;
}

export interface UseDraggableReturn {
  attributes: Record<string, any>;
  listeners: Record<string, any>;
  setNodeRef: (element: HTMLElement | null) => void;
  transform: { x: number; y: number; scaleX: number; scaleY: number } | null;
  isDragging: boolean;
}

// Re-export commonly used dnd-kit types
export type {
  Active,
  Over,
  DragStartEvent,
  DragEndEvent,
  DragOverEvent,
  DragCancelEvent,
} from '@dnd-kit/core';