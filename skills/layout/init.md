# AI-Assisted Component Library: Layout Systems & Responsive Design
## Master Plan for Layout Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025

---

## Executive Summary

Layout systems provide the structural foundation for interfaces. This skill covers grid systems, flexbox patterns, container queries, spacing systems, and responsive design strategies.

---

## Core Concepts

### Grid Systems

**12-Column Grid**
- Traditional responsive grid
- Column spans (col-6 = 50% width)
- Gutter spacing
- **Frameworks:** Bootstrap, Tailwind

**CSS Grid**
- Modern 2D layout
- `grid-template-columns`, `grid-template-rows`
- Gap spacing
- **Best for:** Complex layouts, dashboard grids

**Masonry Grid**
- Pinterest-style layout
- Variable height items
- Efficient space usage
- **Libraries:** Masonry.js, react-masonry

---

### Flexbox Patterns

**Holy Grail Layout**
- Header + 3-column body + footer
- Flexible middle column
- Fixed sidebars

**Sticky Footer**
- Footer at bottom even with little content
- `min-height: 100vh` + flex

**Centering**
- Horizontal: `justify-content: center`
- Vertical: `align-items: center`
- Both: Flexbox or Grid

---

### Container Queries (Modern)

**Problem:** Responsive based on viewport, not container

**Solution:**
```css
@container (min-width: 400px) {
  .card { grid-template-columns: 1fr 1fr; }
}
```

**Benefits:**
- Component-based responsiveness
- Reusable across contexts
- True modular design

---

## Spacing Systems

**Consistent Scale**
- Base unit (4px or 8px)
- Multiples: 4, 8, 12, 16, 24, 32, 48, 64
- Named tokens: `space-xs`, `space-sm`, `space-md`

**Applying:**
- Margin, padding, gap
- Vertical rhythm
- Whitespace hierarchy

---

## Responsive Strategies

**Breakpoints:**
- Mobile: <640px
- Tablet: 640px-1024px
- Desktop: 1024px-1536px
- XL: >1536px

**Approach:**
- Mobile-first (min-width media queries)
- Content-based breakpoints
- Container queries for components

---

## Skill Structure

```yaml
---
name: layout-systems
description: Component library for layout systems and responsive design. Covers grid systems (12-column, CSS Grid, masonry), flexbox patterns (Holy Grail, sticky footer, centering), container queries, spacing systems, and responsive strategies. Includes modern CSS techniques, breakpoint management, and mobile-first design.
---
```

---

## Styling & Theming

### Design Token Integration

All layout components use the **design-tokens** skill for visual styling. Layout tokens define structural spacing, breakpoints, and container sizing that all other components inherit.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Spacing Tokens (Primary Focus):**
- `--container-max-width` - Maximum content width
- `--container-padding-x` - Container horizontal padding
- `--container-padding-y` - Container vertical padding
- `--grid-gap` - Grid column/row gap
- `--grid-columns` - Number of grid columns
- `--section-spacing` - Space between major sections
- `--content-spacing` - Space between content blocks

**Breakpoint Tokens:**
- `--breakpoint-sm` - Small devices (640px)
- `--breakpoint-md` - Medium devices (768px)
- `--breakpoint-lg` - Large devices (1024px)
- `--breakpoint-xl` - Extra large devices (1280px)
- `--breakpoint-2xl` - 2X large devices (1536px)

**Layout-Specific:**
- `--header-height` - Fixed header height
- `--sidebar-width` - Sidebar width
- `--footer-height` - Footer height

### Component-Specific Tokens

```css
/* Container System */
--container-max-width: 1280px;
--container-padding-x: var(--spacing-lg);
--container-padding-y: var(--spacing-md);

/* Grid System */
--grid-columns: 12;
--grid-gap: var(--spacing-md);
--grid-row-gap: var(--spacing-md);

/* Spacing Scale */
--section-spacing: var(--spacing-2xl);
--content-spacing: var(--spacing-lg);

/* Common Layouts */
--header-height: 64px;
--sidebar-width: 280px;
--sidebar-collapsed-width: 64px;
--footer-height: 200px;

/* Responsive Breakpoints */
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

### Theme Support

- ✅ **Responsive Layouts** - Mobile-first with token-based breakpoints
- ✅ **Container Queries** - Component-based responsive design
- ✅ **Flexible Grids** - Token-based grid configuration
- ✅ **Custom Spacing** - Override spacing tokens for dense/spacious layouts

### Example: Custom Layout Theming

```css
/* Dense layout theme */
:root[data-theme="dense-layout"] {
  --container-padding-x: var(--spacing-sm);
  --grid-gap: var(--spacing-sm);
  --section-spacing: var(--spacing-lg);
}

/* Spacious layout theme */
:root[data-theme="spacious-layout"] {
  --container-padding-x: var(--spacing-2xl);
  --grid-gap: var(--spacing-xl);
  --section-spacing: var(--spacing-3xl);
}
```

### Accessibility via Tokens

- **Consistent Spacing**: Predictable layout rhythm aids navigation
- **Touch Targets**: Spacing tokens ensure minimum 44px touch areas
- **Focus Management**: Layout spacing accommodates focus indicators
- **Responsive Text**: Spacing scales with font size

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate library recommendations.

---

## Recommended Libraries & Tools

### **Primary: Native CSS** (No Library Needed)

**Modern CSS (2025):**
- **CSS Grid** - Two-dimensional layouts
- **Flexbox** - One-dimensional layouts
- **Container Queries** - Component-responsive (production-ready all browsers)

**Frameworks (if needed):**
- Tailwind CSS (utility-first)
- Bootstrap (component-based)

**Recommendation:** Use native CSS Grid + Flexbox + Container Queries with design tokens. No library needed.

---

**END OF MASTER PLAN**
