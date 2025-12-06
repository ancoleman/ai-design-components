# Layout Patterns Reference


## Table of Contents

- [Common Layout Patterns](#common-layout-patterns)
  - [Sidebar Layout (Admin Dashboard)](#sidebar-layout-admin-dashboard)
  - [Masonry Grid Layout](#masonry-grid-layout)
  - [Split-Pane Layout](#split-pane-layout)
  - [Holy Grail Layout](#holy-grail-layout)
  - [Card Grid Layout](#card-grid-layout)
- [Layout Composition Patterns](#layout-composition-patterns)
  - [Nested Containers](#nested-containers)
  - [Responsive Stack](#responsive-stack)
- [Performance Considerations](#performance-considerations)
  - [Avoiding Layout Thrashing](#avoiding-layout-thrashing)
  - [CSS Containment](#css-containment)

## Common Layout Patterns

### Sidebar Layout (Admin Dashboard)

The most common application shell pattern.

```tsx
// React component with collapsible sidebar
interface SidebarLayoutProps {
  children: React.ReactNode;
  sidebarContent: React.ReactNode;
  headerContent: React.ReactNode;
}

export function SidebarLayout({ children, sidebarContent, headerContent }: SidebarLayoutProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="layout">
      <header className="layout__header">
        {headerContent}
      </header>
      <div className="layout__body">
        <aside className={`layout__sidebar ${isCollapsed ? 'collapsed' : ''}`}>
          <button
            className="sidebar-toggle"
            onClick={() => setIsCollapsed(!isCollapsed)}
            aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {isCollapsed ? '→' : '←'}
          </button>
          {sidebarContent}
        </aside>
        <main className="layout__main">
          {children}
        </main>
      </div>
    </div>
  );
}
```

```css
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.layout__header {
  height: var(--header-height, 64px);
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-color);
}

.layout__body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.layout__sidebar {
  width: var(--sidebar-width, 280px);
  flex-shrink: 0;
  overflow-y: auto;
  transition: width 0.3s ease;
  border-right: 1px solid var(--border-color);
}

.layout__sidebar.collapsed {
  width: var(--sidebar-collapsed-width, 64px);
}

.layout__main {
  flex: 1;
  overflow-y: auto;
  padding: var(--content-spacing);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .layout__sidebar {
    position: fixed;
    left: 0;
    top: var(--header-height, 64px);
    bottom: 0;
    z-index: 10;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .layout__sidebar.open {
    transform: translateX(0);
  }
}
```

### Masonry Grid Layout

Pinterest-style layout with variable height items.

```tsx
// CSS-only masonry (modern browsers)
export function MasonryGrid({ items }: { items: Array<{ id: string; content: ReactNode; }> }) {
  return (
    <div className="masonry">
      {items.map(item => (
        <div key={item.id} className="masonry__item">
          {item.content}
        </div>
      ))}
    </div>
  );
}
```

```css
/* CSS Grid Masonry (experimental, check browser support) */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-auto-rows: 10px;
  gap: var(--grid-gap);
}

.masonry__item {
  grid-row-end: span var(--item-rows); /* Calculate based on content height */
}

/* Fallback: Column-based masonry */
@supports not (grid-template-rows: masonry) {
  .masonry {
    column-count: 4;
    column-gap: var(--grid-gap);
  }

  @media (max-width: 1200px) { .masonry { column-count: 3; } }
  @media (max-width: 900px) { .masonry { column-count: 2; } }
  @media (max-width: 600px) { .masonry { column-count: 1; } }

  .masonry__item {
    break-inside: avoid;
    margin-bottom: var(--grid-gap);
  }
}
```

### Split-Pane Layout

Resizable panels for editors and comparison views.

```tsx
export function SplitPane({
  left,
  right,
  defaultPosition = 50,
  min = 20,
  max = 80
}: SplitPaneProps) {
  const [position, setPosition] = useState(defaultPosition);
  const containerRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging.current || !containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = (x / rect.width) * 100;

    setPosition(Math.max(min, Math.min(max, percentage)));
  };

  const handleMouseUp = () => {
    isDragging.current = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  };

  const handleMouseDown = () => {
    isDragging.current = true;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  return (
    <div ref={containerRef} className="split-pane">
      <div className="split-pane__left" style={{ width: `${position}%` }}>
        {left}
      </div>
      <div
        className="split-pane__divider"
        onMouseDown={handleMouseDown}
        role="separator"
        aria-valuenow={position}
        aria-valuemin={min}
        aria-valuemax={max}
      />
      <div className="split-pane__right" style={{ width: `${100 - position}%` }}>
        {right}
      </div>
    </div>
  );
}
```

```css
.split-pane {
  display: flex;
  height: 100%;
  position: relative;
}

.split-pane__left,
.split-pane__right {
  overflow: auto;
}

.split-pane__divider {
  width: 4px;
  background: var(--border-color);
  cursor: col-resize;
  position: relative;
  flex-shrink: 0;
}

.split-pane__divider:hover {
  background: var(--primary-color);
}

.split-pane__divider::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: -4px;
  right: -4px;
}
```

### Holy Grail Layout

Classic layout with header, footer, and three-column body.

```tsx
export function HolyGrailLayout({
  header,
  footer,
  nav,
  main,
  aside
}: HolyGrailProps) {
  return (
    <div className="holy-grail">
      <header className="holy-grail__header">
        {header}
      </header>
      <div className="holy-grail__body">
        <nav className="holy-grail__nav">
          {nav}
        </nav>
        <main className="holy-grail__main">
          {main}
        </main>
        <aside className="holy-grail__aside">
          {aside}
        </aside>
      </div>
      <footer className="holy-grail__footer">
        {footer}
      </footer>
    </div>
  );
}
```

```css
.holy-grail {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.holy-grail__header,
.holy-grail__footer {
  flex-shrink: 0;
}

.holy-grail__body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.holy-grail__nav,
.holy-grail__aside {
  flex: 0 0 var(--sidebar-width, 200px);
}

.holy-grail__main {
  flex: 1;
  overflow-y: auto;
  min-width: 0;
}

/* Responsive: Stack on mobile */
@media (max-width: 768px) {
  .holy-grail__body {
    flex-direction: column;
  }

  .holy-grail__nav,
  .holy-grail__aside {
    flex: 0 0 auto;
    width: 100%;
  }
}
```

### Card Grid Layout

Responsive card grid with consistent spacing.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--grid-gap);
  container-type: inline-size;
}

/* Container query for card internals */
@container (min-width: 400px) {
  .card {
    grid-template-columns: auto 1fr;
  }
}

/* Responsive columns based on container */
@container (min-width: 900px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@container (min-width: 1200px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## Layout Composition Patterns

### Nested Containers

```css
.app-shell {
  display: grid;
  grid-template-areas:
    "header header"
    "nav main"
    "nav footer";
  grid-template-columns: var(--sidebar-width) 1fr;
  grid-template-rows: var(--header-height) 1fr var(--footer-height);
  height: 100vh;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; overflow: auto; }
.footer { grid-area: footer; }
```

### Responsive Stack

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

@media (min-width: 768px) {
  .stack--horizontal-md {
    flex-direction: row;
  }
}

.stack > * {
  flex: 1;
}
```

## Performance Considerations

### Avoiding Layout Thrashing

```typescript
// Bad: Forces multiple reflows
elements.forEach(el => {
  el.style.left = el.offsetLeft + 10 + 'px';
  el.style.top = el.offsetTop + 10 + 'px';
});

// Good: Batch reads then writes
const positions = elements.map(el => ({
  left: el.offsetLeft,
  top: el.offsetTop
}));

elements.forEach((el, i) => {
  el.style.left = positions[i].left + 10 + 'px';
  el.style.top = positions[i].top + 10 + 'px';
});
```

### CSS Containment

```css
.card {
  contain: layout style paint;
}

.sidebar {
  contain: layout;
  content-visibility: auto;
}
```