# Touch and Mobile Support for Drag-and-Drop

## Table of Contents
- [Touch Event Handling](#touch-event-handling)
- [Long Press Detection](#long-press-detection)
- [Scroll Prevention](#scroll-prevention)
- [Touch-Friendly UI](#touch-friendly-ui)
- [Gesture Conflict Resolution](#gesture-conflict-resolution)
- [Mobile-Specific Optimizations](#mobile-specific-optimizations)

## Touch Event Handling

### Basic Touch Implementation

```tsx
function useTouchDrag() {
  const [isDragging, setIsDragging] = useState(false);
  const [dragPosition, setDragPosition] = useState({ x: 0, y: 0 });
  const [startPosition, setStartPosition] = useState({ x: 0, y: 0 });
  const elementRef = useRef<HTMLDivElement>(null);

  const handleTouchStart = (e: React.TouchEvent) => {
    const touch = e.touches[0];
    setStartPosition({ x: touch.clientX, y: touch.clientY });
    setDragPosition({ x: touch.clientX, y: touch.clientY });
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging) return;

    e.preventDefault(); // Prevent scrolling
    const touch = e.touches[0];
    setDragPosition({ x: touch.clientX, y: touch.clientY });

    // Update element position
    if (elementRef.current) {
      const deltaX = touch.clientX - startPosition.x;
      const deltaY = touch.clientY - startPosition.y;
      elementRef.current.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    }
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    setIsDragging(false);

    // Find drop target
    const touch = e.changedTouches[0];
    const dropTarget = document.elementFromPoint(touch.clientX, touch.clientY);

    if (dropTarget?.classList.contains('drop-zone')) {
      // Handle drop
      console.log('Dropped on:', dropTarget);
    }

    // Reset position
    if (elementRef.current) {
      elementRef.current.style.transform = '';
    }
  };

  return {
    elementRef,
    touchHandlers: {
      onTouchStart: handleTouchStart,
      onTouchMove: handleTouchMove,
      onTouchEnd: handleTouchEnd,
    },
    isDragging,
    dragPosition,
  };
}
```

### Touch Sensor for dnd-kit

```tsx
import { PointerSensor } from '@dnd-kit/core';

class TouchSensor extends PointerSensor {
  static activators = [
    {
      eventName: 'onTouchStart' as const,
      handler: ({ nativeEvent }: any) => {
        if (nativeEvent.touches?.length !== 1) {
          return false; // Only single touch
        }
        return true;
      },
    },
  ];

  // Long press activation for mobile
  static activationConstraint = {
    delay: 250, // 250ms long press
    tolerance: 5, // 5px movement tolerance during delay
  };
}

// Use in DndContext
const sensors = useSensors(
  useSensor(TouchSensor, {
    activationConstraint: {
      delay: 250,
      tolerance: 5,
    },
  }),
  useSensor(PointerSensor, {
    activationConstraint: {
      distance: 10, // Desktop activation
    },
  })
);
```

## Long Press Detection

### Long Press Hook

```tsx
interface LongPressOptions {
  delay?: number;
  onStart?: () => void;
  onFinish?: () => void;
  onCancel?: () => void;
  moveThreshold?: number;
}

function useLongPress(
  callback: () => void,
  options: LongPressOptions = {}
) {
  const {
    delay = 300,
    onStart,
    onFinish,
    onCancel,
    moveThreshold = 10,
  } = options;

  const [longPressTriggered, setLongPressTriggered] = useState(false);
  const timeout = useRef<NodeJS.Timeout>();
  const target = useRef<EventTarget>();
  const startPosition = useRef({ x: 0, y: 0 });

  const start = useCallback((event: TouchEvent | MouseEvent) => {
    // Store initial position
    const point = 'touches' in event ? event.touches[0] : event;
    startPosition.current = { x: point.clientX, y: point.clientY };

    target.current = event.target;
    timeout.current = setTimeout(() => {
      onStart?.();
      setLongPressTriggered(true);
      callback();
    }, delay);
  }, [callback, delay, onStart]);

  const clear = useCallback((shouldTriggerClick = true) => {
    if (timeout.current) {
      clearTimeout(timeout.current);
      timeout.current = undefined;
    }

    if (longPressTriggered) {
      onFinish?.();
    } else if (!shouldTriggerClick) {
      onCancel?.();
    }

    setLongPressTriggered(false);
  }, [longPressTriggered, onFinish, onCancel]);

  const move = useCallback((event: TouchEvent | MouseEvent) => {
    if (!startPosition.current) return;

    const point = 'touches' in event ? event.touches[0] : event;
    const deltaX = Math.abs(point.clientX - startPosition.current.x);
    const deltaY = Math.abs(point.clientY - startPosition.current.y);

    // Cancel if moved too much
    if (deltaX > moveThreshold || deltaY > moveThreshold) {
      clear(false);
    }
  }, [clear, moveThreshold]);

  return {
    onMouseDown: (e: React.MouseEvent) => start(e.nativeEvent),
    onMouseUp: () => clear(),
    onMouseMove: (e: React.MouseEvent) => move(e.nativeEvent),
    onMouseLeave: () => clear(false),
    onTouchStart: (e: React.TouchEvent) => start(e.nativeEvent),
    onTouchEnd: () => clear(),
    onTouchMove: (e: React.TouchEvent) => move(e.nativeEvent),
  };
}
```

### Visual Feedback for Long Press

```tsx
function LongPressDraggable({ children, onDragStart }) {
  const [isActivating, setIsActivating] = useState(false);
  const [progress, setProgress] = useState(0);
  const animationRef = useRef<number>();

  const startActivation = () => {
    setIsActivating(true);
    const startTime = Date.now();
    const duration = 300; // 300ms activation

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min(elapsed / duration, 1);
      setProgress(newProgress);

      if (newProgress < 1) {
        animationRef.current = requestAnimationFrame(animate);
      }
    };

    animationRef.current = requestAnimationFrame(animate);
  };

  const cancelActivation = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    setIsActivating(false);
    setProgress(0);
  };

  const longPressProps = useLongPress(
    () => {
      setIsActivating(false);
      onDragStart();
    },
    {
      delay: 300,
      onStart: startActivation,
      onCancel: cancelActivation,
    }
  );

  return (
    <div className="long-press-draggable" {...longPressProps}>
      {children}

      {isActivating && (
        <div className="activation-overlay">
          <svg className="progress-ring">
            <circle
              r="20"
              cx="24"
              cy="24"
              fill="none"
              stroke="var(--color-primary)"
              strokeWidth="3"
              strokeDasharray={`${progress * 126} 126`}
              transform="rotate(-90 24 24)"
            />
          </svg>
        </div>
      )}
    </div>
  );
}
```

## Scroll Prevention

### Preventing Scroll During Drag

```tsx
function useScrollLock(isLocked: boolean) {
  useEffect(() => {
    if (!isLocked) return;

    // Store original styles
    const originalStyle = {
      overflow: document.body.style.overflow,
      touchAction: document.body.style.touchAction,
      userSelect: document.body.style.userSelect,
      webkitUserSelect: document.body.style.webkitUserSelect,
    };

    // Prevent scrolling
    document.body.style.overflow = 'hidden';
    document.body.style.touchAction = 'none';
    document.body.style.userSelect = 'none';
    document.body.style.webkitUserSelect = 'none';

    // Prevent iOS bounce
    const preventScroll = (e: TouchEvent) => {
      e.preventDefault();
    };

    document.addEventListener('touchmove', preventScroll, { passive: false });

    return () => {
      // Restore original styles
      document.body.style.overflow = originalStyle.overflow;
      document.body.style.touchAction = originalStyle.touchAction;
      document.body.style.userSelect = originalStyle.userSelect;
      document.body.style.webkitUserSelect = originalStyle.webkitUserSelect;

      document.removeEventListener('touchmove', preventScroll);
    };
  }, [isLocked]);
}
```

### Selective Scroll Prevention

```tsx
function DraggableWithScrollControl({ children }) {
  const [isDragging, setIsDragging] = useState(false);
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!elementRef.current) return;

    const element = elementRef.current;

    const preventScroll = (e: TouchEvent) => {
      // Only prevent scroll if dragging this element
      if (isDragging) {
        e.preventDefault();
        e.stopPropagation();
      }
    };

    // Add to specific element, not document
    element.addEventListener('touchmove', preventScroll, { passive: false });

    return () => {
      element.removeEventListener('touchmove', preventScroll);
    };
  }, [isDragging]);

  return (
    <div
      ref={elementRef}
      className="draggable-scroll-control"
      onTouchStart={() => setIsDragging(true)}
      onTouchEnd={() => setIsDragging(false)}
      style={{
        touchAction: isDragging ? 'none' : 'auto',
      }}
    >
      {children}
    </div>
  );
}
```

## Touch-Friendly UI

### Minimum Touch Target Sizes

```css
/* iOS Human Interface Guidelines: 44x44px minimum */
/* Material Design: 48x48dp minimum */

.touch-draggable {
  min-width: 44px;
  min-height: 44px;
  padding: 12px;

  /* Expand touch area without visual change */
  position: relative;
}

.touch-draggable::before {
  content: '';
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
  /* Invisible touch target extension */
}

.drag-handle-touch {
  /* Larger drag handle for touch */
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;

  /* Visual feedback on touch */
  transition: transform 0.2s, background 0.2s;
}

.drag-handle-touch:active {
  transform: scale(1.1);
  background: var(--color-primary-100);
}

/* Responsive sizing */
@media (pointer: coarse) {
  /* Touch devices */
  .draggable-item {
    padding: 16px;
    margin: 8px 0;
  }

  .drag-handle {
    width: 48px;
    height: 48px;
  }
}

@media (pointer: fine) {
  /* Mouse devices */
  .draggable-item {
    padding: 8px;
    margin: 4px 0;
  }

  .drag-handle {
    width: 32px;
    height: 32px;
  }
}
```

### Touch-Optimized Components

```tsx
function TouchOptimizedDraggable({ item, onDrag }) {
  const [isTouchDevice] = useState(() => 'ontouchstart' in window);

  return (
    <div
      className={`draggable-item ${isTouchDevice ? 'touch-mode' : 'mouse-mode'}`}
      role="button"
      tabIndex={0}
      aria-label={`Drag to reorder ${item.label}`}
    >
      {/* Larger drag handle for touch */}
      <button
        className="drag-handle"
        aria-label="Drag handle"
        style={{
          width: isTouchDevice ? 48 : 32,
          height: isTouchDevice ? 48 : 32,
        }}
      >
        {isTouchDevice ? (
          // Larger icon for touch
          <svg width="24" height="24" viewBox="0 0 24 24">
            <circle cx="8" cy="6" r="2" fill="currentColor" />
            <circle cx="16" cy="6" r="2" fill="currentColor" />
            <circle cx="8" cy="12" r="2" fill="currentColor" />
            <circle cx="16" cy="12" r="2" fill="currentColor" />
            <circle cx="8" cy="18" r="2" fill="currentColor" />
            <circle cx="16" cy="18" r="2" fill="currentColor" />
          </svg>
        ) : (
          // Smaller icon for mouse
          '⋮⋮'
        )}
      </button>

      <div className="item-content">{item.content}</div>

      {isTouchDevice && (
        // Additional touch controls
        <div className="touch-controls">
          <button onClick={() => onDrag('up')} aria-label="Move up">
            ↑
          </button>
          <button onClick={() => onDrag('down')} aria-label="Move down">
            ↓
          </button>
        </div>
      )}
    </div>
  );
}
```

## Gesture Conflict Resolution

### Handling Swipe vs Drag

```tsx
function useGestureDetection() {
  const [gesture, setGesture] = useState<'tap' | 'swipe' | 'drag' | null>(null);
  const startPoint = useRef({ x: 0, y: 0, time: 0 });
  const isDragging = useRef(false);

  const handleTouchStart = (e: TouchEvent) => {
    const touch = e.touches[0];
    startPoint.current = {
      x: touch.clientX,
      y: touch.clientY,
      time: Date.now(),
    };
    isDragging.current = false;
  };

  const handleTouchMove = (e: TouchEvent) => {
    if (!startPoint.current) return;

    const touch = e.touches[0];
    const deltaX = touch.clientX - startPoint.current.x;
    const deltaY = touch.clientY - startPoint.current.y;
    const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);

    if (distance > 10 && !isDragging.current) {
      isDragging.current = true;
      setGesture('drag');
    }
  };

  const handleTouchEnd = (e: TouchEvent) => {
    const touch = e.changedTouches[0];
    const deltaX = touch.clientX - startPoint.current.x;
    const deltaY = touch.clientY - startPoint.current.y;
    const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);
    const duration = Date.now() - startPoint.current.time;

    if (distance < 10 && duration < 200) {
      setGesture('tap');
    } else if (distance > 50 && duration < 300) {
      // Swipe detection
      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        setGesture('swipe');
        // Horizontal swipe (deltaX > 0 ? 'right' : 'left')
      } else {
        setGesture('swipe');
        // Vertical swipe (deltaY > 0 ? 'down' : 'up')
      }
    }

    // Reset after gesture
    setTimeout(() => setGesture(null), 100);
  };

  return {
    gesture,
    handlers: {
      onTouchStart: handleTouchStart,
      onTouchMove: handleTouchMove,
      onTouchEnd: handleTouchEnd,
    },
  };
}
```

### Preventing Pull-to-Refresh

```tsx
function PreventPullToRefresh({ children }) {
  useEffect(() => {
    let lastY = 0;

    const preventPullToRefresh = (e: TouchEvent) => {
      const touch = e.touches[0];
      const deltaY = touch.clientY - lastY;

      // If scrolling up at the top of the page
      if (window.scrollY === 0 && deltaY > 0) {
        e.preventDefault();
      }

      lastY = touch.clientY;
    };

    document.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        lastY = e.touches[0].clientY;
      }
    }, { passive: false });

    document.addEventListener('touchmove', preventPullToRefresh, { passive: false });

    return () => {
      document.removeEventListener('touchstart', () => {});
      document.removeEventListener('touchmove', preventPullToRefresh);
    };
  }, []);

  return <>{children}</>;
}
```

## Mobile-Specific Optimizations

### Performance Optimization for Mobile

```tsx
function MobileOptimizedDraggable({ items }) {
  const [isReducedMotion] = useState(() =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );

  // Use transform for better performance
  const dragStyle = {
    transform: 'translate3d(0, 0, 0)', // Enable hardware acceleration
    willChange: 'transform', // Hint to browser
    backfaceVisibility: 'hidden', // Prevent flickering
  };

  // Throttle drag updates on mobile
  const throttledDragMove = useThrottle((position) => {
    // Update position at 30fps on mobile (vs 60fps on desktop)
    updatePosition(position);
  }, 33);

  return (
    <div className="mobile-optimized-container">
      {items.map(item => (
        <div
          key={item.id}
          style={dragStyle}
          className={`draggable-item ${isReducedMotion ? 'no-animation' : ''}`}
        >
          {item.content}
        </div>
      ))}
    </div>
  );
}
```

### Device Capability Detection

```tsx
function useDeviceCapabilities() {
  const [capabilities, setCapabilities] = useState({
    hasTouch: false,
    hasMouse: false,
    hasHover: false,
    isSmallScreen: false,
    supportsPassive: false,
  });

  useEffect(() => {
    // Detect touch support
    const hasTouch = 'ontouchstart' in window ||
      navigator.maxTouchPoints > 0;

    // Detect mouse support
    const hasMouse = window.matchMedia('(pointer: fine)').matches;

    // Detect hover capability
    const hasHover = window.matchMedia('(hover: hover)').matches;

    // Detect screen size
    const isSmallScreen = window.innerWidth < 768;

    // Detect passive event support
    let supportsPassive = false;
    try {
      const opts = Object.defineProperty({}, 'passive', {
        get: () => {
          supportsPassive = true;
          return true;
        },
      });
      window.addEventListener('test', null as any, opts);
      window.removeEventListener('test', null as any, opts);
    } catch (e) {}

    setCapabilities({
      hasTouch,
      hasMouse,
      hasHover,
      isSmallScreen,
      supportsPassive,
    });
  }, []);

  return capabilities;
}

// Use capabilities to optimize UI
function AdaptiveDragDrop() {
  const { hasTouch, hasHover, isSmallScreen } = useDeviceCapabilities();

  return (
    <DndContext
      sensors={useSensors(
        hasTouch
          ? useSensor(TouchSensor, { activationConstraint: { delay: 250 } })
          : useSensor(PointerSensor, { activationConstraint: { distance: 10 } })
      )}
    >
      <div className={`drag-container ${isSmallScreen ? 'mobile' : 'desktop'}`}>
        {/* Adapt UI based on capabilities */}
        {hasHover && <div className="hover-instructions">Hover to see options</div>}
        {hasTouch && <div className="touch-instructions">Long press to drag</div>}
      </div>
    </DndContext>
  );
}
```

### iOS-Specific Fixes

```css
/* Prevent iOS tap highlight */
.draggable-item {
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
}

/* Fix iOS momentum scrolling */
.scroll-container {
  -webkit-overflow-scrolling: touch;
  overflow-y: auto;
}

/* Prevent iOS zoom on double tap */
.touch-target {
  touch-action: manipulation;
}

/* iOS safe area handling */
.drag-container {
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```