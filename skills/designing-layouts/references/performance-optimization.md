# Layout Performance Optimization

## Avoiding Layout Thrashing

Layout thrashing occurs when JavaScript repeatedly reads and writes to the DOM, forcing multiple reflows.

### The Problem

```javascript
// Bad: Causes layout thrashing
function updatePositions(elements) {
  elements.forEach(el => {
    // Read (forces reflow)
    const left = el.offsetLeft;
    const top = el.offsetTop;

    // Write (invalidates layout)
    el.style.left = (left + 10) + 'px';
    el.style.top = (top + 10) + 'px';
  });
}
```

### The Solution

```javascript
// Good: Batch reads, then batch writes
function updatePositions(elements) {
  // Batch all reads first
  const positions = elements.map(el => ({
    element: el,
    left: el.offsetLeft,
    top: el.offsetTop
  }));

  // Then batch all writes
  positions.forEach(({ element, left, top }) => {
    element.style.left = (left + 10) + 'px';
    element.style.top = (top + 10) + 'px';
  });
}

// Better: Use transform instead of left/top
function updatePositionsOptimized(elements) {
  elements.forEach(el => {
    // Transform doesn't trigger layout
    el.style.transform = 'translate(10px, 10px)';
  });
}
```

### Using requestAnimationFrame

```javascript
// Optimize with requestAnimationFrame
class LayoutOptimizer {
  constructor() {
    this.reads = [];
    this.writes = [];
    this.scheduled = false;
  }

  read(fn) {
    this.reads.push(fn);
    this.scheduleUpdate();
  }

  write(fn) {
    this.writes.push(fn);
    this.scheduleUpdate();
  }

  scheduleUpdate() {
    if (!this.scheduled) {
      this.scheduled = true;
      requestAnimationFrame(() => this.runTasks());
    }
  }

  runTasks() {
    const reads = [...this.reads];
    const writes = [...this.writes];

    this.reads = [];
    this.writes = [];
    this.scheduled = false;

    // Execute all reads
    reads.forEach(read => read());

    // Then execute all writes
    writes.forEach(write => write());
  }
}

// Usage
const optimizer = new LayoutOptimizer();

optimizer.read(() => {
  const width = element.offsetWidth;
  optimizer.write(() => {
    element.style.width = (width * 2) + 'px';
  });
});
```

## CSS Containment

CSS Containment isolates parts of the DOM to improve performance.

### Layout Containment

```css
/* Isolate layout calculations */
.card {
  contain: layout;
}

/* The browser knows changes inside .card won't affect outside layout */
.card:hover {
  /* Internal changes don't trigger parent reflow */
  padding: 20px;
}
```

### Size Containment

```css
/* Element has intrinsic size */
.fixed-component {
  contain: size;
  width: 300px;
  height: 400px;
}

/* Children changes don't affect parent */
.fixed-component > * {
  /* Can change without parent reflow */
  transform: scale(1.1);
}
```

### Style Containment

```css
/* Counters and quotes don't escape */
.isolated-content {
  contain: style;
}

/* Paint containment - no visual overflow */
.clipped {
  contain: paint;
}

/* Strict containment (all types) */
.fully-contained {
  contain: strict;
}

/* Content-visibility for off-screen content */
.lazy-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* Estimated size */
}
```

## Optimizing Large Lists

### Virtual Scrolling

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

export function VirtualList({ items }: { items: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated item height
    overscan: 5, // Render 5 items outside viewport
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {items[virtualItem.index]}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Intersection Observer for Lazy Loading

```typescript
export function useLazyLoad(threshold = 0.1) {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsIntersecting(entry.isIntersecting);
      },
      { threshold }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [threshold]);

  return { ref, isIntersecting };
}

// Usage
function LazySection({ children }) {
  const { ref, isIntersecting } = useLazyLoad();

  return (
    <section ref={ref}>
      {isIntersecting ? children : <div style={{ minHeight: '400px' }} />}
    </section>
  );
}
```

## Optimizing CSS

### Efficient Selectors

```css
/* Bad: Descendant selectors are slow */
.sidebar ul li a {
  color: blue;
}

/* Good: Direct class */
.sidebar-link {
  color: blue;
}

/* Bad: Universal selector */
* {
  box-sizing: border-box;
}

/* Good: Inheritance or specific */
html {
  box-sizing: border-box;
}
*, *::before, *::after {
  box-sizing: inherit;
}

/* Bad: Attribute selectors can be slow */
[data-state="active"] {
  color: red;
}

/* Good: Class selector */
.is-active {
  color: red;
}
```

### Reduce Paint Complexity

```css
/* Use transform instead of position changes */
.animate-position {
  /* Bad: Triggers layout */
  left: 100px;

  /* Good: Only triggers composite */
  transform: translateX(100px);
}

/* Use opacity for fading */
.fade {
  /* Bad: Triggers paint */
  background-color: rgba(0, 0, 0, 0.5);

  /* Good: Only triggers composite */
  opacity: 0.5;
}

/* Layer promotion for animations */
.will-animate {
  will-change: transform, opacity;
  /* Creates new layer, improves animation performance */
}

/* Remove will-change after animation */
.animation-complete {
  will-change: auto;
}
```

## Responsive Images Performance

### Native Lazy Loading

```html
<!-- Modern lazy loading -->
<img
  src="image.jpg"
  loading="lazy"
  decoding="async"
  width="800"
  height="600"
  alt="Description"
>

<!-- Responsive with lazy loading -->
<picture>
  <source
    media="(max-width: 768px)"
    srcset="mobile.webp"
    type="image/webp"
  >
  <source
    media="(max-width: 768px)"
    srcset="mobile.jpg"
    type="image/jpeg"
  >
  <img
    src="desktop.jpg"
    loading="lazy"
    decoding="async"
    alt="Description"
  >
</picture>
```

### Progressive Image Loading

```typescript
export function ProgressiveImage({ src, placeholder, alt }) {
  const [imageSrc, setImageSrc] = useState(placeholder);
  const [imageRef, setImageRef] = useState<HTMLImageElement>();

  useEffect(() => {
    const img = new Image();
    img.src = src;
    img.onload = () => {
      setImageSrc(src);
      if (imageRef) {
        imageRef.classList.add('loaded');
      }
    };
  }, [src]);

  return (
    <div className="progressive-image">
      <img
        ref={setImageRef}
        src={imageSrc}
        alt={alt}
        className="image"
      />
    </div>
  );
}
```

```css
.progressive-image {
  position: relative;
  overflow: hidden;
}

.progressive-image .image {
  filter: blur(5px);
  transition: filter 0.3s;
}

.progressive-image .image.loaded {
  filter: blur(0);
}
```

## Memory Management

### Cleanup Event Listeners

```typescript
export function useOptimizedResize(callback: () => void) {
  useEffect(() => {
    let rafId: number;
    let resizeTimeout: NodeJS.Timeout;

    const handleResize = () => {
      // Cancel any pending animation frame
      if (rafId) {
        cancelAnimationFrame(rafId);
      }

      // Debounce resize events
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        rafId = requestAnimationFrame(callback);
      }, 100);
    };

    window.addEventListener('resize', handleResize, { passive: true });

    return () => {
      window.removeEventListener('resize', handleResize);
      if (rafId) {
        cancelAnimationFrame(rafId);
      }
      clearTimeout(resizeTimeout);
    };
  }, [callback]);
}
```

### Optimize Re-renders

```typescript
// Memoize expensive calculations
const MemoizedGrid = React.memo(({ items, columns }) => {
  const gridItems = useMemo(() => {
    return items.map(item => ({
      ...item,
      gridColumn: `span ${Math.ceil(columns / item.size)}`
    }));
  }, [items, columns]);

  return (
    <div className="grid">
      {gridItems.map(item => (
        <div key={item.id} style={{ gridColumn: item.gridColumn }}>
          {item.content}
        </div>
      ))}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.columns === nextProps.columns &&
         prevProps.items.length === nextProps.items.length;
});
```

## Critical CSS

### Inline Critical Styles

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Critical CSS for above-the-fold content */
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
    }

    .header {
      height: 64px;
      display: flex;
      align-items: center;
    }

    @media (max-width: 768px) {
      .container {
        padding: 0 15px;
      }
    }
  </style>

  <!-- Load non-critical CSS asynchronously -->
  <link
    rel="preload"
    href="/css/main.css"
    as="style"
    onload="this.onload=null;this.rel='stylesheet'"
  >
  <noscript>
    <link rel="stylesheet" href="/css/main.css">
  </noscript>
</head>
</html>
```

## Performance Monitoring

```typescript
// Monitor layout performance
export function useLayoutPerformance(componentName: string) {
  useEffect(() => {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'measure') {
          console.log(`${componentName} layout took ${entry.duration}ms`);
        }
      }
    });

    observer.observe({ entryTypes: ['measure'] });

    // Measure layout time
    performance.mark(`${componentName}-start`);

    return () => {
      performance.mark(`${componentName}-end`);
      performance.measure(
        componentName,
        `${componentName}-start`,
        `${componentName}-end`
      );
      observer.disconnect();
    };
  }, [componentName]);
}
```