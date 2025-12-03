# Styling & Theming Integration Guide

## Purpose

This document describes how component skills integrate with the `theming-components` skill for consistent, themeable styling across all 29 skills.

## Status

**All 29 skills are complete and integrated with the theming system.**

### Frontend Skills (15/15)
- `theming-components` - Foundational theming skill (design tokens source)
- `visualizing-data` - Charts, graphs, data visualization
- `building-tables` - Tables and data grids
- `creating-dashboards` - Dashboard layouts and analytics
- `building-forms` - Form systems and validation
- `implementing-search-filter` - Search and filter interfaces
- `building-ai-chat` - AI chat interfaces
- `implementing-drag-drop` - Drag-and-drop functionality
- `providing-feedback` - Feedback and notifications
- `implementing-navigation` - Navigation patterns
- `designing-layouts` - Layout systems and responsive design
- `displaying-timelines` - Timeline and activity components
- `managing-media` - Media and file management
- `guiding-users` - Onboarding and help systems
- `assembling-components` - Component integration and validation

### Backend Skills (14/14)
Backend skills reference theming tokens for any UI components they generate (admin panels, API documentation, etc.).

---

## Core Architecture

### Token Hierarchy (3 Levels)

```
Primitive Tokens     → Raw values (--color-blue-500: #3B82F6)
        ↓
Semantic Tokens      → Purpose-based (--color-primary: var(--color-blue-500))
        ↓
Component Tokens     → Component-specific (--button-bg-primary: var(--color-primary))
```

### Token Categories (7 Core)

| Category | Purpose | Example |
|----------|---------|---------|
| Color | All color values | `--color-primary`, `--color-error` |
| Spacing | Margins, padding, gaps | `--spacing-md`, `--space-4` |
| Typography | Fonts, sizes, weights | `--font-size-base`, `--font-weight-bold` |
| Borders | Widths, styles | `--border-width-thin`, `--radius-md` |
| Shadows | Elevation, depth | `--shadow-md`, `--shadow-focus-primary` |
| Motion | Transitions, animations | `--duration-fast`, `--transition-fast` |
| Z-Index | Stacking order | `--z-modal`, `--z-tooltip` |

---

## Component Token Naming Convention

```
--{component}-{property}-{variant?}-{state?}
```

**Examples:**
- `--button-bg-primary` - Button background, primary variant
- `--button-bg-primary-hover` - Button background, primary variant, hover state
- `--input-border-color-focus` - Input border color, focus state
- `--chart-color-1` - Chart color palette, first color

---

## Component-Specific Token Reference

### Data Visualization (`visualizing-data`)
```css
--chart-primary-color: var(--color-primary);
--chart-secondary-color: var(--color-secondary);
--chart-axis-color: var(--color-text-secondary);
--chart-grid-color: var(--color-border);
--chart-tooltip-bg: var(--color-gray-900);
--chart-tooltip-text: var(--color-white);
--chart-color-1: var(--color-blue-500);
--chart-color-2: var(--color-green-500);
--chart-color-3: var(--color-amber-500);
```

### Tables (`building-tables`)
```css
--table-bg: var(--color-white);
--table-header-bg: var(--color-gray-50);
--table-row-hover-bg: var(--color-gray-100);
--table-border-color: var(--color-border);
--table-cell-padding: var(--spacing-md);
--table-sort-icon-color: var(--color-text-secondary);
```

### Dashboards (`creating-dashboards`)
```css
--dashboard-bg: var(--color-bg-secondary);
--widget-bg: var(--color-white);
--widget-shadow: var(--shadow-md);
--widget-border-radius: var(--radius-lg);
--kpi-value-color: var(--color-text-primary);
--kpi-trend-positive: var(--color-success);
--kpi-trend-negative: var(--color-error);
```

### Forms (`building-forms`)
```css
--input-bg: var(--color-white);
--input-border-color: var(--color-border);
--input-border-color-focus: var(--color-primary);
--input-text-color: var(--color-text-primary);
--input-placeholder-color: var(--color-text-tertiary);
--input-error-color: var(--color-error);
--input-padding: var(--spacing-sm) var(--spacing-md);
```

### Search & Filter (`implementing-search-filter`)
```css
--search-input-bg: var(--color-white);
--search-icon-color: var(--color-text-secondary);
--filter-chip-bg: var(--color-gray-100);
--filter-chip-bg-active: var(--color-primary-50);
--filter-dropdown-shadow: var(--shadow-lg);
```

### AI Chat (`building-ai-chat`)
```css
--chat-bg: var(--color-bg-primary);
--chat-user-bubble-bg: var(--color-primary);
--chat-user-bubble-text: var(--color-white);
--chat-ai-bubble-bg: var(--color-gray-100);
--chat-ai-bubble-text: var(--color-text-primary);
--chat-typing-indicator-color: var(--color-text-secondary);
--chat-input-bg: var(--color-white);
```

### Drag & Drop (`implementing-drag-drop`)
```css
--draggable-cursor: grab;
--dragging-cursor: grabbing;
--drop-zone-border-color: var(--color-border);
--drop-zone-border-color-active: var(--color-primary);
--drop-zone-bg-active: var(--color-primary-50);
--dragged-item-opacity: 0.5;
--drag-handle-color: var(--color-text-tertiary);
```

### Feedback (`providing-feedback`)
```css
--toast-bg: var(--color-gray-900);
--toast-text: var(--color-white);
--toast-shadow: var(--shadow-xl);
--alert-success-bg: var(--color-success-bg);
--alert-error-bg: var(--color-error-bg);
--alert-warning-bg: var(--color-warning-bg);
--modal-backdrop-bg: rgba(0, 0, 0, 0.5);
--modal-bg: var(--color-white);
```

### Navigation (`implementing-navigation`)
```css
--nav-bg: var(--color-white);
--nav-border-color: var(--color-border);
--nav-item-color: var(--color-text-primary);
--nav-item-hover-bg: var(--color-gray-100);
--nav-item-active-bg: var(--color-primary-50);
--nav-item-active-color: var(--color-primary);
--nav-mobile-menu-bg: var(--color-white);
```

### Layout (`designing-layouts`)
```css
--layout-max-width: 1280px;
--layout-gutter: var(--spacing-md);
--container-padding: var(--spacing-lg);
--grid-gap: var(--spacing-md);
--sidebar-width: 256px;
--header-height: 64px;
```

### Timeline (`displaying-timelines`)
```css
--timeline-line-color: var(--color-border);
--timeline-dot-color: var(--color-primary);
--timeline-dot-size: 12px;
--timeline-item-bg: var(--color-white);
--timeline-item-shadow: var(--shadow-sm);
--timestamp-color: var(--color-text-secondary);
```

### Media (`managing-media`)
```css
--image-border-radius: var(--radius-md);
--image-shadow: var(--shadow-md);
--video-player-bg: var(--color-black);
--video-controls-bg: rgba(0, 0, 0, 0.7);
--upload-zone-border-color: var(--color-border);
--upload-zone-border-color-active: var(--color-primary);
--upload-progress-color: var(--color-primary);
```

### Onboarding (`guiding-users`)
```css
--tour-spotlight-bg: var(--color-white);
--tour-spotlight-shadow: var(--shadow-2xl);
--tour-overlay-bg: rgba(0, 0, 0, 0.7);
--tour-progress-color: var(--color-primary);
--tooltip-bg: var(--color-gray-900);
--tooltip-text: var(--color-white);
--hint-bg: var(--color-primary-50);
```

---

## Theme Support

All component tokens automatically adapt to themes:

### Built-in Themes
- **Light Mode** - Default bright theme
- **Dark Mode** - Dark backgrounds, light text
- **High Contrast** - WCAG AAA compliance (7:1 contrast)
- **Custom Brand** - Override tokens for brand identity

### Theme Switching

```javascript
// Set theme
document.documentElement.setAttribute('data-theme', 'dark');

// Toggle theme
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  document.documentElement.setAttribute('data-theme',
    current === 'dark' ? 'light' : 'dark'
  );
}
```

### Dark Mode Example

```css
:root[data-theme="dark"] {
  /* Semantic tokens automatically adjust */
  --color-bg-primary: var(--color-gray-900);
  --color-bg-secondary: var(--color-gray-800);
  --color-text-primary: var(--color-gray-50);
  --color-border: var(--color-gray-700);

  /* Component tokens use semantics - no changes needed! */
}
```

---

## RTL/i18n Support

Use CSS logical properties for automatic RTL language support:

| Physical (Avoid) | Logical (Use) |
|------------------|---------------|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |

**Example:**
```css
.button {
  padding-inline: var(--button-padding-inline);
  margin-inline-start: var(--spacing-sm);
}
```

---

## Accessibility Tokens

### Focus States
```css
--focus-ring-color: var(--color-primary);
--focus-ring-width: 2px;
--focus-ring-offset: 2px;
--shadow-focus-primary: 0 0 0 3px rgba(59, 130, 246, 0.3);
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --transition-fast: none;
  }
}
```

### High Contrast
```css
:root[data-theme="high-contrast"] {
  --color-primary: #0000FF;
  --color-text-primary: #000000;
  --color-bg-primary: #FFFFFF;
  /* 7:1+ contrast ratios */
}
```

---

## Integration Checklist

When creating or updating a component skill:

- [ ] Use CSS custom properties for ALL visual styling
- [ ] Follow naming convention: `--{component}-{property}-{variant?}-{state?}`
- [ ] Reference semantic tokens, not primitive values
- [ ] Use CSS logical properties for spacing/alignment
- [ ] Include focus state tokens for accessibility
- [ ] Test with light, dark, and high-contrast themes
- [ ] Verify reduced motion support

---

## Reference Documents

**In `skills/theming-components/`:**
- `SKILL.md` - Main theming skill documentation
- `references/color-system.md` - Complete color scales
- `references/typography-system.md` - Type system
- `references/spacing-system.md` - Spacing scale
- `references/theme-switching.md` - Theme implementation
- `references/component-integration.md` - Integration patterns
- `references/logical-properties.md` - RTL support
- `references/accessibility-tokens.md` - WCAG compliance
- `references/style-dictionary-setup.md` - Multi-platform export

---

*This guide ensures consistent styling across all 29 skills while enabling theme customization and accessibility compliance.*
