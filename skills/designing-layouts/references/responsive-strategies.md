# Responsive Design Strategies


## Table of Contents

- [Mobile-First Approach](#mobile-first-approach)
  - [Benefits](#benefits)
  - [Implementation](#implementation)
- [Breakpoint Strategy](#breakpoint-strategy)
  - [Content-Based Breakpoints](#content-based-breakpoints)
  - [Standard Breakpoint System](#standard-breakpoint-system)
  - [CSS Custom Properties for Breakpoints](#css-custom-properties-for-breakpoints)
- [Fluid Typography](#fluid-typography)
  - [Clamp() for Responsive Text](#clamp-for-responsive-text)
  - [Viewport Units with Limits](#viewport-units-with-limits)
- [Container Queries](#container-queries)
  - [Component-Level Responsiveness](#component-level-responsiveness)
  - [Named Containers](#named-containers)
- [Responsive Images](#responsive-images)
  - [Modern Picture Element](#modern-picture-element)
  - [Responsive Background Images](#responsive-background-images)
- [Responsive Tables](#responsive-tables)
  - [Overflow Scrolling](#overflow-scrolling)
  - [Stacked Layout on Mobile](#stacked-layout-on-mobile)
- [Responsive Navigation](#responsive-navigation)
  - [Progressive Disclosure Pattern](#progressive-disclosure-pattern)
- [Performance Optimization](#performance-optimization)
  - [Responsive Loading](#responsive-loading)
  - [CSS Grid with Subgrid](#css-grid-with-subgrid)
- [Testing Responsive Designs](#testing-responsive-designs)
  - [Viewport Testing Checklist](#viewport-testing-checklist)
  - [Orientation Testing](#orientation-testing)

## Mobile-First Approach

Start with mobile layout and progressively enhance for larger screens.

### Benefits
- Smaller initial CSS payload
- Progressive enhancement mindset
- Better performance on mobile devices
- Forces content prioritization

### Implementation

```css
/* Base styles (mobile) */
.container {
  width: 100%;
  padding: var(--spacing-sm);
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    max-width: 750px;
    padding: var(--spacing-md);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    padding: var(--spacing-lg);
  }
}
```

## Breakpoint Strategy

### Content-Based Breakpoints

Set breakpoints based on content needs, not device sizes.

```css
/* When the navigation becomes cramped */
@media (min-width: 580px) {
  .nav {
    flex-direction: row;
  }
}

/* When cards look better side-by-side */
@media (min-width: 620px) {
  .card-container {
    grid-template-columns: 1fr 1fr;
  }
}
```

### Standard Breakpoint System

```javascript
// breakpoints.config.js
export const breakpoints = {
  xs: '320px',   // Small phones
  sm: '640px',   // Large phones
  md: '768px',   // Tablets
  lg: '1024px',  // Desktops
  xl: '1280px',  // Large desktops
  '2xl': '1536px' // Wide screens
};
```

### CSS Custom Properties for Breakpoints

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Usage with container queries */
@container (min-width: 640px) {
  .component {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

## Fluid Typography

### Clamp() for Responsive Text

```css
:root {
  /* Fluid typography that scales between viewports */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.8rem + 2.25vw, 3rem);
}

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
p { font-size: var(--text-base); }
```

### Viewport Units with Limits

```css
.hero-title {
  /* Minimum 2rem, maximum 4rem, scales with viewport */
  font-size: clamp(2rem, 5vw, 4rem);

  /* Line height that scales appropriately */
  line-height: clamp(1.2, 1.1 + 0.1vw, 1.4);
}
```

## Container Queries

### Component-Level Responsiveness

```css
/* Container setup */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Respond to container size, not viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
    gap: var(--spacing-md);
  }

  .card__image {
    width: 150px;
    height: 150px;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr auto;
  }

  .card__actions {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }
}
```

### Named Containers

```css
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

.main-content {
  container-type: inline-size;
  container-name: main;
}

/* Different behavior based on container */
@container sidebar (max-width: 300px) {
  .nav-item__label {
    display: none;
  }
}

@container main (min-width: 800px) {
  .content-grid {
    grid-template-columns: 2fr 1fr;
  }
}
```

## Responsive Images

### Modern Picture Element

```html
<picture>
  <!-- WebP for browsers that support it -->
  <source
    type="image/webp"
    srcset="image-sm.webp 640w,
            image-md.webp 1024w,
            image-lg.webp 1920w"
    sizes="(max-width: 640px) 100vw,
           (max-width: 1024px) 50vw,
           33vw"
  >
  <!-- Fallback to JPEG -->
  <source
    type="image/jpeg"
    srcset="image-sm.jpg 640w,
            image-md.jpg 1024w,
            image-lg.jpg 1920w"
    sizes="(max-width: 640px) 100vw,
           (max-width: 1024px) 50vw,
           33vw"
  >
  <!-- Final fallback -->
  <img
    src="image-md.jpg"
    alt="Description"
    loading="lazy"
    decoding="async"
    width="1024"
    height="768"
  >
</picture>
```

### Responsive Background Images

```css
.hero {
  background-image: url('hero-mobile.jpg');
  background-size: cover;
  background-position: center;
}

@media (min-width: 768px) and (min-resolution: 1dppx) {
  .hero {
    background-image: url('hero-tablet.jpg');
  }
}

@media (min-width: 768px) and (min-resolution: 2dppx) {
  .hero {
    background-image: url('hero-tablet@2x.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-desktop.jpg');
  }
}
```

## Responsive Tables

### Overflow Scrolling

```css
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table {
  min-width: 600px;
}
```

### Stacked Layout on Mobile

```css
@media (max-width: 768px) {
  .table,
  .table tbody,
  .table tr,
  .table td {
    display: block;
    width: 100%;
  }

  .table tr {
    margin-bottom: var(--spacing-md);
    border: 1px solid var(--border-color);
  }

  .table td {
    display: flex;
    justify-content: space-between;
    padding: var(--spacing-sm);
  }

  .table td::before {
    content: attr(data-label);
    font-weight: bold;
  }
}
```

## Responsive Navigation

### Progressive Disclosure Pattern

```tsx
export function ResponsiveNav({ items }: { items: NavItem[] }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="nav">
      <button
        className="nav__toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-label="Toggle navigation"
      >
        <span className="nav__toggle-icon" />
      </button>

      <ul className={`nav__list ${isOpen ? 'nav__list--open' : ''}`}>
        {items.map(item => (
          <li key={item.id} className="nav__item">
            <a href={item.href} className="nav__link">
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

```css
/* Mobile first */
.nav__toggle {
  display: block;
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 100;
}

.nav__list {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--background-color);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.nav__list--open {
  transform: translateX(0);
}

/* Desktop */
@media (min-width: 768px) {
  .nav__toggle {
    display: none;
  }

  .nav__list {
    position: static;
    transform: none;
    display: flex;
    gap: var(--spacing-md);
  }
}
```

## Performance Optimization

### Responsive Loading

```tsx
function ResponsiveComponent() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkDevice = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkDevice();
    window.addEventListener('resize', checkDevice);
    return () => window.removeEventListener('resize', checkDevice);
  }, []);

  return (
    <>
      {isMobile ? (
        <MobileComponent />
      ) : (
        <DesktopComponent />
      )}
    </>
  );
}
```

### CSS Grid with Subgrid

```css
.layout {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gap);
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
}
```

## Testing Responsive Designs

### Viewport Testing Checklist

- [ ] 320px (small phone)
- [ ] 375px (iPhone)
- [ ] 414px (large phone)
- [ ] 768px (tablet)
- [ ] 1024px (desktop)
- [ ] 1440px (large desktop)
- [ ] 1920px (full HD)

### Orientation Testing

```css
/* Portrait orientation */
@media (orientation: portrait) {
  .video-player {
    width: 100%;
    height: auto;
  }
}

/* Landscape orientation */
@media (orientation: landscape) {
  .video-player {
    width: 70%;
    margin: 0 auto;
  }
}
```