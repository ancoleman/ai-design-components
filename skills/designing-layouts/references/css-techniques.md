# Modern CSS Techniques


## Table of Contents

- [CSS Grid](#css-grid)
  - [Grid Fundamentals](#grid-fundamentals)
  - [Advanced Grid Patterns](#advanced-grid-patterns)
  - [Grid Alignment](#grid-alignment)
- [Flexbox](#flexbox)
  - [Flexbox Patterns](#flexbox-patterns)
  - [Advanced Flexbox](#advanced-flexbox)
- [Container Queries](#container-queries)
  - [Basic Container Queries](#basic-container-queries)
  - [Container Query Units](#container-query-units)
  - [Nested Containers](#nested-containers)
- [CSS Custom Properties (Variables)](#css-custom-properties-variables)
  - [Dynamic Properties](#dynamic-properties)
  - [Property Manipulation](#property-manipulation)
- [Modern Layout Features](#modern-layout-features)
  - [Aspect Ratio](#aspect-ratio)
  - [Logical Properties](#logical-properties)
  - [CSS Subgrid](#css-subgrid)
  - [Scroll Snap](#scroll-snap)
- [CSS Math Functions](#css-math-functions)
  - [Clamp, Min, Max](#clamp-min-max)
  - [Calc with Custom Properties](#calc-with-custom-properties)
- [Performance Techniques](#performance-techniques)
  - [Content Visibility](#content-visibility)
  - [CSS Containment](#css-containment)
  - [Will-Change](#will-change)

## CSS Grid

### Grid Fundamentals

```css
/* Basic grid setup */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr auto;
  gap: var(--grid-gap);
}

/* Named grid lines */
.grid-advanced {
  display: grid;
  grid-template-columns:
    [full-start] minmax(1rem, 1fr)
    [content-start] minmax(0, 80ch)
    [content-end] minmax(1rem, 1fr)
    [full-end];
}

/* Grid template areas */
.app-layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav main aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }
```

### Advanced Grid Patterns

```css
/* Auto-fit with minimum size */
.auto-grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(250px, 100%), 1fr)
  );
  gap: var(--grid-gap);
}

/* Asymmetric grid */
.featured-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--grid-gap);
}

.featured-grid > :nth-child(1) {
  grid-column: span 4;
  grid-row: span 2;
}

.featured-grid > :nth-child(2),
.featured-grid > :nth-child(3) {
  grid-column: span 2;
}

/* RAM (Repeat, Auto, Minmax) pattern */
.ram-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: clamp(1rem, 2vw, 2rem);
}
```

### Grid Alignment

```css
/* Alignment within grid */
.grid-aligned {
  display: grid;
  place-items: center; /* Centers all items */

  /* Or individually */
  justify-items: start; /* Horizontal alignment */
  align-items: end;     /* Vertical alignment */

  /* Or for the whole grid */
  justify-content: space-between;
  align-content: center;
}

/* Individual item alignment */
.grid-item {
  justify-self: end;
  align-self: center;
}
```

## Flexbox

### Flexbox Patterns

```css
/* Centering */
.center-flex {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Space between with alignment */
.nav-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

/* Flex grow/shrink/basis */
.flex-item {
  flex: 1 1 300px; /* grow shrink basis */
}

/* Sticky footer with flexbox */
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page__content {
  flex: 1;
}

.page__footer {
  flex-shrink: 0;
}
```

### Advanced Flexbox

```css
/* Equal height columns */
.card-container {
  display: flex;
  gap: var(--spacing-md);
}

.card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card__content {
  flex: 1;
}

/* Wrapping with basis */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.flex-wrap > * {
  flex: 1 1 calc(33.333% - var(--spacing-md));
  min-width: 250px;
}

/* Order manipulation */
.flex-reorder {
  display: flex;
}

.flex-reorder__important {
  order: -1; /* Moves to front */
}

@media (max-width: 768px) {
  .flex-reorder__sidebar {
    order: 1; /* Moves to end on mobile */
  }
}
```

## Container Queries

### Basic Container Queries

```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query container size */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

@container card (min-width: 700px) {
  .card {
    grid-template-columns: 200px 1fr 150px;
  }
}

/* Style queries */
@container style(--theme: dark) {
  .card {
    background: var(--dark-background);
    color: var(--dark-text);
  }
}
```

### Container Query Units

```css
/* Container query units */
.responsive-text {
  /* cqw = container query width */
  font-size: clamp(1rem, 5cqw, 2rem);

  /* cqh = container query height */
  padding: 2cqh 4cqw;

  /* cqi = container query inline size */
  /* cqb = container query block size */
  margin: 2cqb 4cqi;

  /* cqmin/cqmax */
  width: 80cqmin; /* 80% of smaller dimension */
}
```

### Nested Containers

```css
.outer-container {
  container-type: inline-size;
  container-name: outer;
}

.inner-container {
  container-type: inline-size;
  container-name: inner;
}

@container outer (min-width: 800px) {
  .outer-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}

@container inner (min-width: 400px) {
  .inner-content {
    font-size: 1.2rem;
  }
}
```

## CSS Custom Properties (Variables)

### Dynamic Properties

```css
/* Scoped custom properties */
.component {
  --component-spacing: var(--spacing-md);
  --component-radius: 8px;
  --component-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  padding: var(--component-spacing);
  border-radius: var(--component-radius);
  box-shadow: var(--component-shadow);
}

/* Computed properties */
.dynamic {
  --columns: 3;
  --gap: 20px;
  --total-gap: calc((var(--columns) - 1) * var(--gap));
  --column-width: calc((100% - var(--total-gap)) / var(--columns));

  display: grid;
  grid-template-columns: repeat(var(--columns), 1fr);
  gap: var(--gap);
}

/* Fallback values */
.safe-properties {
  color: var(--text-color, #333);
  background: var(--bg-color, white);
  padding: var(--padding, 1rem);
}
```

### Property Manipulation

```css
/* Space toggles */
.theme-switch {
  --theme-primary: var(--light-primary);
  --theme-background: var(--light-background);
  --theme-text: var(--light-text);
}

.theme-switch[data-theme="dark"] {
  --theme-primary: var(--dark-primary);
  --theme-background: var(--dark-background);
  --theme-text: var(--dark-text);
}

/* Responsive properties */
.responsive-var {
  --size: 1rem;
}

@media (min-width: 768px) {
  .responsive-var {
    --size: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .responsive-var {
    --size: 2rem;
  }
}

.responsive-var > * {
  font-size: var(--size);
  padding: calc(var(--size) * 0.5);
}
```

## Modern Layout Features

### Aspect Ratio

```css
/* Maintain aspect ratios */
.aspect-ratio {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover;
}

.square {
  aspect-ratio: 1;
}

.golden-ratio {
  aspect-ratio: 1.618;
}

/* Responsive aspect ratio */
.responsive-aspect {
  aspect-ratio: 1;
}

@media (min-width: 768px) {
  .responsive-aspect {
    aspect-ratio: 4 / 3;
  }
}

@media (min-width: 1024px) {
  .responsive-aspect {
    aspect-ratio: 16 / 9;
  }
}
```

### Logical Properties

```css
/* Physical properties (avoid) */
.old-way {
  margin-left: 1rem;
  padding-right: 2rem;
  border-top: 1px solid;
}

/* Logical properties (preferred) */
.modern-way {
  margin-inline-start: 1rem;
  padding-inline-end: 2rem;
  border-block-start: 1px solid;
}

/* Shorthand logical properties */
.logical-shorthand {
  margin-inline: auto; /* left and right */
  padding-block: 2rem; /* top and bottom */

  /* Equivalent to width/height in horizontal writing */
  inline-size: 100%;
  block-size: 50vh;

  /* Min/max logical */
  min-inline-size: 250px;
  max-block-size: 400px;
}
```

### CSS Subgrid

```css
/* Parent grid */
.parent-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: repeat(4, minmax(100px, auto));
  gap: 1rem;
}

/* Child inherits parent grid */
.subgrid-item {
  display: grid;
  grid-column: span 6;
  grid-row: span 2;

  /* Inherits parent's columns and rows */
  grid-template-columns: subgrid;
  grid-template-rows: subgrid;
}

/* Nested elements align to parent grid */
.subgrid-item > * {
  grid-column: span 2;
}
```

### Scroll Snap

```css
/* Horizontal scroll snap */
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  gap: 1rem;
}

.carousel__item {
  flex: 0 0 100%;
  scroll-snap-align: start;
}

/* Vertical scroll snap */
.sections {
  height: 100vh;
  overflow-y: auto;
  scroll-snap-type: y proximity;
}

.section {
  height: 100vh;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}
```

## CSS Math Functions

### Clamp, Min, Max

```css
/* Responsive sizing with clamp */
.responsive {
  width: clamp(300px, 50%, 800px);
  padding: clamp(1rem, 3vw, 3rem);
  font-size: clamp(1rem, 1rem + 1vw, 1.5rem);
}

/* Min/Max functions */
.flexible {
  width: min(90%, 1200px);
  height: max(300px, 50vh);

  /* Complex calculations */
  padding: min(max(1rem, 2vw), 3rem);
}
```

### Calc with Custom Properties

```css
.calculated {
  --base-size: 1rem;
  --multiplier: 1.5;
  --offset: 0.5rem;

  font-size: calc(var(--base-size) * var(--multiplier) + var(--offset));

  /* Nested calc */
  width: calc(100% - calc(var(--spacing) * 2));

  /* With different units */
  height: calc(100vh - 60px - 2rem);
}
```

## Performance Techniques

### Content Visibility

```css
/* Optimize rendering of off-screen content */
.card {
  content-visibility: auto;
  contain-intrinsic-size: 0 300px; /* Estimated height */
}

/* For sections */
.section {
  content-visibility: auto;
  contain-intrinsic-size: 0 100vh;
}
```

### CSS Containment

```css
/* Isolate layout calculations */
.isolated {
  contain: layout style paint;
}

/* Size containment for fixed dimensions */
.fixed-size {
  contain: size layout style paint;
  width: 300px;
  height: 400px;
}

/* Strict containment */
.strict {
  contain: strict; /* All types except style */
}
```

### Will-Change

```css
/* Optimize for animations */
.will-animate {
  will-change: transform, opacity;
}

/* Remove after animation */
.animated {
  animation: slide-in 0.3s ease;
}

.animated::after {
  will-change: auto;
}
```