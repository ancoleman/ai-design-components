---
sidebar_position: 11
title: Designing Layouts
description: Layout systems and responsive interfaces with grid systems and flexbox patterns
tags: [frontend, layouts, responsive, css-grid, flexbox]
---

# Designing Layout Systems & Responsive Design

Comprehensive guidance for creating responsive layout systems using modern CSS techniques.

## When to Use

Use this skill when:
- Building responsive admin dashboards with sidebars and headers
- Creating grid-based layouts for content cards or galleries
- Implementing masonry or Pinterest-style layouts
- Designing split-pane interfaces with resizable panels
- Establishing responsive breakpoint systems
- Structuring application shells with navigation and content areas
- Building mobile-first responsive designs
- Creating flexible spacing and container systems

## Layout Patterns

### Grid Systems

For structured, two-dimensional layouts, use CSS Grid with design tokens.

**12-Column Grid:**
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gap);
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding-x);
}

.col-span-6 { grid-column: span 6; }
.col-span-4 { grid-column: span 4; }
```

**Auto-Fit Responsive Grid:**
```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
  gap: var(--grid-gap);
}
```

### Flexbox Patterns

For one-dimensional layouts and alignment control.

**Holy Grail Layout:**
```css
.holy-grail {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.holy-grail__body {
  flex: 1;
  display: flex;
}

.holy-grail__nav {
  width: var(--sidebar-width);
  flex-shrink: 0;
}

.holy-grail__main {
  flex: 1;
  min-width: 0; /* Prevent overflow */
}
```

### Container Queries

For component-responsive design that adapts based on container size, not viewport.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    grid-template-columns: auto 1fr;
    gap: var(--spacing-lg);
  }
}
```

Container queries are production-ready in all modern browsers (2025).

## Responsive Breakpoints

Use mobile-first approach with semantic breakpoints.

```css
/* Mobile-first breakpoints using design tokens */
@media (min-width: 640px) {  /* sm: Tablet portrait */
  .container { max-width: 640px; }
}

@media (min-width: 768px) {  /* md: Tablet landscape */
  .container { max-width: 768px; }
}

@media (min-width: 1024px) { /* lg: Desktop */
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) { /* xl: Wide desktop */
  .container { max-width: 1280px; }
}
```

## Spacing Systems

Implement consistent spacing using design tokens.

```css
/* Base unit: 4px or 8px */
:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}

/* Apply systematically */
.section { padding: var(--section-spacing) 0; }
.container { padding: 0 var(--container-padding-x); }
.card { padding: var(--spacing-lg); }
```

## CSS Framework Integration

### Tailwind CSS

For utility-first approach with custom configuration:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        'xs': 'var(--spacing-xs)',
        'sm': 'var(--spacing-sm)',
        'md': 'var(--spacing-md)',
        'lg': 'var(--spacing-lg)',
      },
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
      }
    }
  }
}
```

## How to Use

### 1. Define Layout Requirements

Determine layout type and responsive behavior needed.

### 2. Choose Layout Method

- **CSS Grid**: Two-dimensional layouts, complex grids
- **Flexbox**: One-dimensional layouts, alignment
- **Container Queries**: Component-responsive designs

### 3. Implement with Design Tokens

Use design tokens from the theming-components skill for consistent spacing, breakpoints, and sizing.

### 4. Test Responsiveness

Test across device sizes using responsive preview tools and actual devices.

## Related Skills

- [Theming Components](./theming-components.md) - Spacing and breakpoint tokens
- [Creating Dashboards](./creating-dashboards.md) - Dashboard layout patterns
- [Implementing Navigation](./implementing-navigation.md) - Navigation layout integration
- [Implementing Drag Drop](./implementing-drag-drop.md) - Reorderable layouts

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/designing-layouts)
- Patterns: `references/layout-patterns.md`, `references/css-techniques.md`
- Responsive: `references/responsive-strategies.md`
- Accessibility: `references/accessibility-layouts.md`
- Examples: `examples/admin-layout.tsx`, `examples/responsive-grid.tsx`
