#!/usr/bin/env node

/**
 * Generate dnd-kit Configuration
 * Creates configuration for sensors, modifiers, and animations
 */

// Generate sensor configuration
function generateSensorConfig(options = {}) {
  const {
    enablePointer = true,
    enableKeyboard = true,
    enableTouch = true,
    pointerActivationConstraint = { distance: 10 },
    keyboardCoordinateGetter = 'sortableKeyboardCoordinates',
    touchActivationConstraint = { delay: 250, tolerance: 5 },
  } = options;

  const sensors = [];

  if (enablePointer) {
    sensors.push({
      sensor: 'PointerSensor',
      options: {
        activationConstraint: pointerActivationConstraint,
      },
    });
  }

  if (enableKeyboard) {
    sensors.push({
      sensor: 'KeyboardSensor',
      options: {
        coordinateGetter: keyboardCoordinateGetter,
      },
    });
  }

  if (enableTouch) {
    sensors.push({
      sensor: 'TouchSensor',
      options: {
        activationConstraint: touchActivationConstraint,
      },
    });
  }

  return sensors;
}

// Generate modifier configuration
function generateModifierConfig(options = {}) {
  const {
    restrictToVerticalAxis = false,
    restrictToHorizontalAxis = false,
    restrictToWindowEdges = true,
    restrictToParentElement = false,
    snapToGrid = false,
    gridSize = 20,
  } = options;

  const modifiers = [];

  if (restrictToVerticalAxis) {
    modifiers.push({
      modifier: 'restrictToVerticalAxis',
    });
  }

  if (restrictToHorizontalAxis) {
    modifiers.push({
      modifier: 'restrictToHorizontalAxis',
    });
  }

  if (restrictToWindowEdges) {
    modifiers.push({
      modifier: 'restrictToWindowEdges',
    });
  }

  if (restrictToParentElement) {
    modifiers.push({
      modifier: 'restrictToParentElement',
    });
  }

  if (snapToGrid) {
    modifiers.push({
      modifier: 'snapCenterToCursor',
      options: { gridSize },
    });
  }

  return modifiers;
}

// Generate animation configuration
function generateAnimationConfig(options = {}) {
  const {
    duration = 200,
    easing = 'cubic-bezier(0.4, 0, 0.2, 1)',
    dragOverlay = true,
    dropAnimation = true,
    layoutAnimation = true,
    sideEffects = {
      opacity: 0.5,
      scale: 1.05,
    },
  } = options;

  return {
    duration,
    easing,
    dragOverlay: dragOverlay ? {
      opacity: sideEffects.opacity,
      scale: sideEffects.scale,
    } : null,
    dropAnimation: dropAnimation ? {
      duration: duration * 1.5,
      easing,
      keyframes: [
        { transform: 'scale(1.05)' },
        { transform: 'scale(0.95)' },
        { transform: 'scale(1)' },
      ],
    } : null,
    layoutAnimation: layoutAnimation ? {
      duration,
      easing,
    } : null,
  };
}

// Generate collision detection configuration
function generateCollisionConfig(strategy = 'closestCenter') {
  const strategies = {
    closestCenter: {
      name: 'closestCenter',
      description: 'Drop on the element whose center is closest to the pointer',
    },
    closestCorners: {
      name: 'closestCorners',
      description: 'Drop on the element whose corners are closest',
    },
    rectIntersection: {
      name: 'rectIntersection',
      description: 'Drop on the element with the largest intersection area',
    },
    pointerWithin: {
      name: 'pointerWithin',
      description: 'Drop on the element the pointer is within',
    },
  };

  return strategies[strategy] || strategies.closestCenter;
}

// Generate sorting strategy configuration
function generateSortingStrategy(type = 'vertical') {
  const strategies = {
    vertical: {
      name: 'verticalListSortingStrategy',
      description: 'For vertical lists',
      direction: 'vertical',
    },
    horizontal: {
      name: 'horizontalListSortingStrategy',
      description: 'For horizontal lists',
      direction: 'horizontal',
    },
    grid: {
      name: 'rectSortingStrategy',
      description: 'For grid layouts',
      direction: 'both',
    },
  };

  return strategies[type] || strategies.vertical;
}

// Generate accessibility configuration
function generateAccessibilityConfig(options = {}) {
  const {
    announcements = true,
    liveRegion = true,
    screenReaderInstructions = true,
    ariaDescribedBy = 'dnd-instructions',
  } = options;

  const config = {
    announcements: announcements ? {
      onDragStart: (id) => `Picked up draggable item ${id}`,
      onDragOver: (id, overId) => overId
        ? `Draggable item ${id} is over droppable area ${overId}`
        : `Draggable item ${id} is no longer over a droppable area`,
      onDragEnd: (id, overId) => overId
        ? `Draggable item ${id} was dropped over droppable area ${overId}`
        : `Draggable item ${id} was dropped`,
      onDragCancel: (id) => `Dragging was cancelled. Draggable item ${id} was dropped`,
    } : null,
    liveRegion,
    screenReaderInstructions,
    ariaDescribedBy,
    ariaAttributes: {
      role: 'application',
      'aria-roledescription': 'Sortable list',
    },
  };

  return config;
}

// Generate auto-scroll configuration
function generateAutoScrollConfig(options = {}) {
  const {
    enabled = true,
    threshold = 0.2, // 20% from edge
    maxSpeed = 10,
    acceleration = 10,
    interval = 10,
    canScroll = true,
  } = options;

  if (!enabled) return null;

  return {
    enabled,
    threshold: typeof threshold === 'number' ? { x: threshold, y: threshold } : threshold,
    maxSpeed,
    acceleration,
    interval,
    canScroll: typeof canScroll === 'boolean' ? () => canScroll : canScroll,
  };
}

// Generate complete dnd-kit configuration
function generateCompleteConfig(presetOrOptions = 'default') {
  const presets = {
    default: {
      sensors: { enablePointer: true, enableKeyboard: true },
      modifiers: { restrictToWindowEdges: true },
      animation: { duration: 200 },
      collision: 'closestCenter',
      sorting: 'vertical',
      accessibility: { announcements: true },
      autoScroll: { enabled: true },
    },
    kanban: {
      sensors: { enablePointer: true, enableKeyboard: true, enableTouch: true },
      modifiers: { restrictToWindowEdges: false },
      animation: { duration: 250, dragOverlay: true },
      collision: 'rectIntersection',
      sorting: 'vertical',
      accessibility: { announcements: true },
      autoScroll: { enabled: true, threshold: 0.15 },
    },
    grid: {
      sensors: { enablePointer: true, enableKeyboard: false },
      modifiers: { snapToGrid: true, gridSize: 100 },
      animation: { duration: 150 },
      collision: 'closestCenter',
      sorting: 'grid',
      accessibility: { announcements: true },
      autoScroll: { enabled: false },
    },
    mobile: {
      sensors: {
        enablePointer: false,
        enableTouch: true,
        touchActivationConstraint: { delay: 300, tolerance: 10 },
      },
      modifiers: { restrictToVerticalAxis: true },
      animation: { duration: 300 },
      collision: 'closestCenter',
      sorting: 'vertical',
      accessibility: { announcements: false },
      autoScroll: { enabled: true, maxSpeed: 5 },
    },
  };

  const config = typeof presetOrOptions === 'string'
    ? presets[presetOrOptions] || presets.default
    : presetOrOptions;

  return {
    sensors: generateSensorConfig(config.sensors),
    modifiers: generateModifierConfig(config.modifiers),
    animation: generateAnimationConfig(config.animation),
    collision: generateCollisionConfig(config.collision),
    sorting: generateSortingStrategy(config.sorting),
    accessibility: generateAccessibilityConfig(config.accessibility),
    autoScroll: generateAutoScrollConfig(config.autoScroll),
  };
}

// Generate TypeScript types for configuration
function generateTypeScriptTypes() {
  return `
// dnd-kit Configuration Types
export interface DndConfig {
  sensors: SensorConfig[];
  modifiers: ModifierConfig[];
  animation: AnimationConfig;
  collision: CollisionConfig;
  sorting: SortingConfig;
  accessibility: AccessibilityConfig;
  autoScroll: AutoScrollConfig | null;
}

export interface SensorConfig {
  sensor: 'PointerSensor' | 'KeyboardSensor' | 'TouchSensor';
  options?: {
    activationConstraint?: {
      distance?: number;
      delay?: number;
      tolerance?: number;
    };
    coordinateGetter?: string;
  };
}

export interface ModifierConfig {
  modifier: string;
  options?: Record<string, any>;
}

export interface AnimationConfig {
  duration: number;
  easing: string;
  dragOverlay: {
    opacity: number;
    scale: number;
  } | null;
  dropAnimation: {
    duration: number;
    easing: string;
    keyframes: Keyframe[];
  } | null;
  layoutAnimation: {
    duration: number;
    easing: string;
  } | null;
}

export interface CollisionConfig {
  name: string;
  description: string;
}

export interface SortingConfig {
  name: string;
  description: string;
  direction: 'vertical' | 'horizontal' | 'both';
}

export interface AccessibilityConfig {
  announcements: {
    onDragStart: (id: string) => string;
    onDragOver: (id: string, overId?: string) => string;
    onDragEnd: (id: string, overId?: string) => string;
    onDragCancel: (id: string) => string;
  } | null;
  liveRegion: boolean;
  screenReaderInstructions: boolean;
  ariaDescribedBy: string;
  ariaAttributes: Record<string, string>;
}

export interface AutoScrollConfig {
  enabled: boolean;
  threshold: { x: number; y: number };
  maxSpeed: number;
  acceleration: number;
  interval: number;
  canScroll: () => boolean;
}
`;
}

// Main function for CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    console.log(`
Generate dnd-kit Configuration

Usage:
  node generate_dnd_config.js [preset] [--format json|js|ts]

Presets:
  default   Basic sortable list configuration
  kanban    Kanban board configuration
  grid      Grid layout configuration
  mobile    Mobile-optimized configuration

Options:
  --format  Output format (json, js, or ts)
  --help    Show this help message

Examples:
  node generate_dnd_config.js default
  node generate_dnd_config.js kanban --format json
  node generate_dnd_config.js grid --format ts
    `);
    process.exit(0);
  }

  const preset = args[0];
  const formatIndex = args.indexOf('--format');
  const format = formatIndex !== -1 ? args[formatIndex + 1] : 'json';

  const config = generateCompleteConfig(preset);

  switch (format) {
    case 'json':
      console.log(JSON.stringify(config, null, 2));
      break;

    case 'js':
      console.log(`// dnd-kit configuration for ${preset}
export const dndConfig = ${JSON.stringify(config, null, 2)};`);
      break;

    case 'ts':
      console.log(generateTypeScriptTypes());
      console.log(`
// dnd-kit configuration for ${preset}
export const dndConfig: DndConfig = ${JSON.stringify(config, null, 2)};`);
      break;

    default:
      console.error(`Unknown format: ${format}`);
      process.exit(1);
  }
}

// Export functions for use in other scripts
module.exports = {
  generateSensorConfig,
  generateModifierConfig,
  generateAnimationConfig,
  generateCollisionConfig,
  generateSortingStrategy,
  generateAccessibilityConfig,
  generateAutoScrollConfig,
  generateCompleteConfig,
  generateTypeScriptTypes,
};