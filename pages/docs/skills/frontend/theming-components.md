---
sidebar_position: 1
title: Theming Components
description: Design token system and theming framework for consistent, customizable UI styling across all components
tags: [frontend, design-tokens, theming, css-variables]
---

# Theming Components

Comprehensive design token system providing the foundational styling architecture for all component skills, enabling brand customization, theme switching, RTL support, and consistent visual design.

## When to Use

Use this skill when:
- Theming components or implementing light/dark mode
- Creating brand styles or custom design systems
- Customizing visual design with consistent tokens
- Ensuring design consistency across components
- Supporting RTL languages or internationalization
- Building accessible themes (WCAG contrast, high contrast, reduced motion)

## Overview

Design tokens are the **single source of truth** for all visual design decisions. This skill provides:

1. **Complete Token Taxonomy**: 7 core categories (color, typography, spacing, borders, shadows, motion, z-index)
2. **Theme Switching**: Light/dark mode, high-contrast, custom brand themes
3. **RTL/i18n Support**: CSS logical properties for automatic right-to-left language support
4. **Multi-Platform Export**: CSS variables, SCSS, iOS Swift, Android XML, JavaScript
5. **Component Integration**: Skill chaining architecture for consistent styling across all components

## Quick Start

### Using Tokens in Components

```css
.button {
  background-color: var(--button-bg-primary);
  color: var(--button-text-primary);
  padding-inline: var(--button-padding-inline);
  padding-block: var(--button-padding-block);
  border-radius: var(--button-border-radius);
  transition: var(--transition-fast);
}
```

### Basic Theme Switching

```javascript
function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('theme', themeName);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
}
```

## Token Taxonomy (7 Core Categories)

### 1. Color Tokens
3-tier hierarchy: Primitive → Semantic → Component
- 9-shade scales for each base color
- Semantic naming (primary, success, error, warning)
- Component-specific tokens (--button-bg-primary)

### 2. Spacing Tokens
4px base scale with semantic names
- --space-1 through --space-12
- Semantic aliases (--spacing-sm, --spacing-md, --spacing-lg)

### 3. Typography Tokens
Font families, sizes, weights, and line heights
- --font-sans, --font-mono
- --font-size-sm through --font-size-4xl
- --font-weight-normal, --font-weight-semibold, --font-weight-bold

### 4. Border & Radius Tokens
Border widths and corner radius values
- --border-width-thin, --border-width-medium
- --radius-sm through --radius-full

### 5. Shadow Tokens
Elevation and focus shadows
- --shadow-sm, --shadow-md, --shadow-lg
- --shadow-focus-primary for accessibility

### 6. Motion Tokens
Animation durations and easing functions
- --duration-fast, --duration-normal
- --ease-out, --transition-fast
- Respects prefers-reduced-motion

### 7. Z-Index Tokens
Layering system for overlays
- --z-dropdown, --z-modal, --z-tooltip

## Key Features

- **Theme Architecture**: Light/dark themes with custom brand support
- **CSS Logical Properties**: Automatic RTL language support
- **Component Integration**: All component skills use these tokens
- **Accessibility**: WCAG 2.1 AA compliance, high-contrast themes, reduced motion
- **Platform Exports**: Transform tokens to any platform via Style Dictionary
- **W3C Token Format**: Industry-standard token format support

## Decision Framework

**Component Skills (Behavior + Structure) → Use tokens for ALL visual styling**
**Design Tokens (Styling Variables) → Define colors, spacing, typography**
**Theme Files (Token Overrides) → Light, dark, brand-specific values**

## Related Skills

- All frontend skills use design tokens for styling
- [Designing Layouts](./designing-layouts.md) - Layout spacing and breakpoints
- [Visualizing Data](./visualizing-data.md) - Chart color tokens
- [Providing Feedback](./providing-feedback.md) - Alert and toast colors

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/theming-components)
- Token System Reference: `references/color-system.md`, `references/typography-system.md`
- Implementation Guides: `references/theme-switching.md`, `references/component-integration.md`
- Tools: `references/style-dictionary-setup.md`, `references/accessibility-tokens.md`
