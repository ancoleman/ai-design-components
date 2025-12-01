# Design Tokens Skill Chaining Architecture

**Document Version:** 1.0
**Date:** November 13, 2025
**Purpose:** Define HOW component skills consume design tokens for consistent, themeable styling

---

## Executive Summary

This document defines the **foundational architecture** for skill chaining between `design-tokens` and all component skills (`data-viz`, `forms`, `tables`, etc.). It ensures:

- ✅ **Visual consistency** across all components
- ✅ **Automatic theming** (light/dark/high-contrast/custom brands)
- ✅ **RTL support** via CSS logical properties
- ✅ **Zero coupling** between component behavior and visual styling
- ✅ **Infinite customization** without code changes

**Critical Principle:**
```
Component Skills = Behavior + Structure (NO visual styling)
Design Tokens = Visual Styling Variables (colors, spacing, typography)
Themes = Token value overrides (light, dark, brand-specific)
```

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Token Consumption Patterns](#token-consumption-patterns)
3. [Component Token Naming Convention](#component-token-naming-convention)
4. [CSS Logical Properties (RTL Support)](#css-logical-properties-rtl-support)
5. [Theme Switching Mechanism](#theme-switching-mechanism)
6. [Component Integration Checklist](#component-integration-checklist)
7. [Examples](#examples)

---

## Architecture Overview

### The Token Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│ LEVEL 1: PRIMITIVE TOKENS (Foundation)                  │
│ Raw values, not used directly                           │
│                                                          │
│ --color-blue-500: #3B82F6                               │
│ --space-4: 16px                                         │
│ --font-size-base: 16px                                  │
└─────────────────────────────────────────────────────────┘
                         ↓ referenced by
┌─────────────────────────────────────────────────────────┐
│ LEVEL 2: SEMANTIC TOKENS (Purpose)                      │
│ Meaningful names based on role                          │
│                                                          │
│ --color-primary: var(--color-blue-500)                  │
│ --spacing-md: var(--space-4)                            │
│ --text-base: var(--font-size-base)                      │
└─────────────────────────────────────────────────────────┘
                         ↓ referenced by
┌─────────────────────────────────────────────────────────┐
│ LEVEL 3: COMPONENT TOKENS (Specific)                    │
│ Component-specific styling                              │
│                                                          │
│ --button-bg-primary: var(--color-primary)               │
│ --button-padding-inline: var(--spacing-md)              │
│ --button-font-size: var(--text-base)                    │
└─────────────────────────────────────────────────────────┘
                         ↓ used by
┌─────────────────────────────────────────────────────────┐
│ COMPONENT SKILLS (forms, data-viz, tables, etc.)        │
│ Use component tokens for ALL styling                    │
│                                                          │
│ .button {                                               │
│   background: var(--button-bg-primary);                 │
│   padding-inline: var(--button-padding-inline);         │
│   font-size: var(--button-font-size);                   │
│ }                                                        │
└─────────────────────────────────────────────────────────┘
```

---

## Token Consumption Patterns

### Pattern 1: Component Token Usage (Recommended)

**Component skills reference component-specific tokens:**

```tsx
// ✅ CORRECT - Uses component tokens
function Button({ variant = 'primary', children }) {
  return (
    <button
      style={{
        backgroundColor: `var(--button-bg-${variant})`,
        color: `var(--button-text-${variant})`,
        paddingInline: 'var(--button-padding-inline)',
        paddingBlock: 'var(--button-padding-block)',
        borderRadius: 'var(--button-border-radius)',
        fontSize: 'var(--button-font-size)',
        fontWeight: 'var(--button-font-weight)',
        border: 'none',
        cursor: 'pointer',
        transition: 'var(--transition-fast)',
      }}
    >
      {children}
    </button>
  );
}
```

**Why this works:**
- Theme changes automatically apply
- Component stays decoupled from token values
- Brand customization requires NO code changes
- Component tokens can be overridden in themes

---

### Pattern 2: CSS Modules/Stylesheets

```css
/* Button.module.css */
.button {
  background-color: var(--button-bg-primary);
  color: var(--button-text-primary);
  padding-inline: var(--button-padding-inline);
  padding-block: var(--button-padding-block);
  border-radius: var(--button-border-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  border: none;
  cursor: pointer;
  transition: var(--transition-fast);
}

.button:hover {
  background-color: var(--button-bg-primary-hover);
}

.button--secondary {
  background-color: var(--button-bg-secondary);
  color: var(--button-text-secondary);
}

.button:disabled {
  background-color: var(--button-bg-disabled);
  color: var(--button-text-disabled);
  cursor: not-allowed;
}
```

---

### Pattern 3: Semantic Tokens (When No Component Token Exists)

**If a component-specific token isn't defined, use semantic tokens:**

```tsx
// ✅ ACCEPTABLE - Uses semantic tokens as fallback
function Alert({ type = 'info', children }) {
  const bgColor = `var(--color-${type}-bg)`;      // Semantic
  const borderColor = `var(--color-${type}-border)`; // Semantic
  const textColor = `var(--color-${type}-text)`;    // Semantic

  return (
    <div
      style={{
        backgroundColor: bgColor,
        borderInlineStart: `4px solid ${borderColor}`,
        color: textColor,
        padding: 'var(--spacing-md)',
        borderRadius: 'var(--radius-md)',
      }}
    >
      {children}
    </div>
  );
}
```

---

### ❌ Anti-Pattern: Hardcoded Values

```tsx
// ❌ WRONG - Hardcoded values, no theming support
function Button({ children }) {
  return (
    <button
      style={{
        backgroundColor: '#3B82F6',  // ❌ Hardcoded
        color: '#FFFFFF',            // ❌ Hardcoded
        padding: '12px 24px',        // ❌ Hardcoded
        borderRadius: '8px',         // ❌ Hardcoded
        fontSize: '16px',            // ❌ Hardcoded
      }}
    >
      {children}
    </button>
  );
}
```

**Why this is bad:**
- Breaks theme switching
- Requires code changes for brand customization
- No dark mode support
- Inconsistent with other components

---

## Component Token Naming Convention

### Standard Format

```
--{component}-{property}-{variant?}-{state?}
```

**Examples:**
```css
/* Button Component */
--button-bg-primary              /* Background for primary variant */
--button-bg-primary-hover        /* Background on hover */
--button-bg-primary-active       /* Background when active/pressed */
--button-text-primary            /* Text color for primary variant */
--button-padding-inline          /* Horizontal padding (RTL-aware) */
--button-padding-block           /* Vertical padding */
--button-border-radius           /* Corner radius */
--button-font-size               /* Text size */
--button-font-weight             /* Text weight */

/* Input Component */
--input-bg                       /* Background color */
--input-border-color             /* Border color (normal state) */
--input-border-color-focus       /* Border color when focused */
--input-border-color-error       /* Border color for error state */
--input-text-color               /* Text color */
--input-placeholder-color        /* Placeholder text color */
--input-padding-inline           /* Horizontal padding */
--input-height                   /* Fixed height */

/* Chart Component (data-viz skill) */
--chart-color-1                  /* First data series color */
--chart-color-2                  /* Second data series color */
--chart-axis-color               /* Axis line color */
--chart-grid-color               /* Grid line color */
--chart-tooltip-bg               /* Tooltip background */
--chart-font-family              /* Chart text font */
```

### Naming Rules

1. **Always prefix with component name**: `--button-`, `--input-`, `--chart-`
2. **Use logical property names**: `padding-inline`, `margin-block-start` (NOT `padding-left`, `margin-top`)
3. **Include variant if applicable**: `-primary`, `-secondary`, `-tertiary`
4. **Include state if applicable**: `-hover`, `-active`, `-disabled`, `-focus`, `-error`
5. **Be specific and descriptive**: `--button-bg-primary` not `--btn-bg-p`

---

## CSS Logical Properties (RTL Support)

### **CRITICAL: All component skills MUST use logical properties**

**Why?**
- Automatic RTL (Right-to-Left) support for Arabic, Hebrew, Persian, Urdu
- No separate RTL stylesheets needed
- Scales to all languages with zero code changes

### Physical → Logical Mapping

| Physical Property (❌ AVOID) | Logical Property (✅ USE) | Auto-Flips in RTL? |
|------------------------------|---------------------------|--------------------|
| `margin-left`                | `margin-inline-start`     | ✅ Yes             |
| `margin-right`               | `margin-inline-end`       | ✅ Yes             |
| `margin-top`                 | `margin-block-start`      | ❌ No (vertical)   |
| `margin-bottom`              | `margin-block-end`        | ❌ No (vertical)   |
| `padding-left`               | `padding-inline-start`    | ✅ Yes             |
| `padding-right`              | `padding-inline-end`      | ✅ Yes             |
| `border-left`                | `border-inline-start`     | ✅ Yes             |
| `border-right`               | `border-inline-end`       | ✅ Yes             |
| `left: 0`                    | `inset-inline-start: 0`   | ✅ Yes             |
| `right: 0`                   | `inset-inline-end: 0`     | ✅ Yes             |
| `text-align: left`           | `text-align: start`       | ✅ Yes             |
| `text-align: right`          | `text-align: end`         | ✅ Yes             |

### Shorthand Properties

```css
/* Inline (horizontal in LTR, auto-flips in RTL) */
padding-inline: 16px;               /* Both start and end */
margin-inline: 8px 16px;            /* Start, end */

/* Block (vertical, same in all languages) */
padding-block: 12px;                /* Both start and end */
margin-block: 8px 16px;             /* Start, end */
```

### Token Examples with Logical Properties

```css
/* ✅ CORRECT - Uses logical properties */
:root {
  --button-padding-inline: 24px;           /* Horizontal padding */
  --button-padding-block: 12px;            /* Vertical padding */
  --button-margin-inline-start: 8px;       /* Space before button */
  --icon-margin-inline-end: 4px;           /* Space after icon */
  --dropdown-arrow-inset-inline-end: 12px; /* Arrow position */
}

/* Component usage */
.button {
  padding-inline: var(--button-padding-inline);
  padding-block: var(--button-padding-block);
  margin-inline-start: var(--button-margin-inline-start);
}

/* LTR: padding-left: 24px, padding-right: 24px, margin-left: 8px */
/* RTL: padding-right: 24px, padding-left: 24px, margin-right: 8px */
```

```css
/* ❌ WRONG - Uses physical properties */
:root {
  --button-padding-left: 24px;   /* ❌ Won't flip in RTL */
  --button-padding-right: 24px;  /* ❌ Won't flip in RTL */
  --button-margin-left: 8px;     /* ❌ Won't flip in RTL */
}
```

### Browser Support (2025)

**Excellent Support:**
- Chrome/Edge: Since 2018
- Firefox: Since 2018
- Safari: Since 2018
- All modern browsers fully support logical properties

---

## Theme Switching Mechanism

### How It Works

**1. Set `data-theme` attribute on `<html>`:**

```html
<!-- Light theme (default) -->
<html lang="en" data-theme="light">

<!-- Dark theme -->
<html lang="en" data-theme="dark">

<!-- Custom brand theme -->
<html lang="en" data-theme="acme-brand">
```

**2. Theme-specific token overrides:**

```css
/* Base theme (light) */
:root {
  --color-primary: #3B82F6;
  --color-background: #FFFFFF;
  --color-text-primary: #1F2937;
}

/* Dark theme */
:root[data-theme="dark"] {
  --color-primary: #60A5FA;        /* Lighter primary for dark bg */
  --color-background: #111827;     /* Dark background */
  --color-text-primary: #F9FAFB;   /* Light text */
}

/* Brand theme */
:root[data-theme="acme-brand"] {
  --color-primary: #FF6B35;        /* Brand orange */
  --color-secondary: #004E89;      /* Brand blue */
  --font-sans: 'Poppins', sans-serif; /* Brand font */
}
```

**3. JavaScript theme switcher:**

```javascript
// Set theme
function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('theme', themeName);
}

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
setTheme(savedTheme);

// Toggle theme
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  setTheme(next);
}
```

**4. React Theme Provider Pattern:**

```tsx
import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext({
  theme: 'light',
  setTheme: (theme: string) => {},
});

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);

// Usage in component
function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
    </button>
  );
}
```

---

## Component Integration Checklist

When creating or updating a component skill, follow this checklist:

### ✅ Design Phase
- [ ] Identify all visual styling properties (colors, spacing, typography, etc.)
- [ ] Map properties to token categories (color, spacing, typography, border, shadow, motion)
- [ ] Define component-specific tokens in naming convention
- [ ] Document token usage in component init.md

### ✅ Implementation Phase
- [ ] Use CSS custom properties for ALL styling (`var(--token-name)`)
- [ ] Use logical properties for layout (`padding-inline`, `margin-block`)
- [ ] NO hardcoded color values
- [ ] NO hardcoded spacing values
- [ ] NO hardcoded font sizes
- [ ] NO `margin-left`, `padding-right`, etc. (use logical properties)

### ✅ Token Definition Phase
- [ ] Define component tokens in `design-tokens/tokens/components/{component}.json`
- [ ] Use W3C format: `$value`, `$type`, `$description`
- [ ] Reference semantic tokens (not primitives directly)
- [ ] Include all variants (primary, secondary, etc.)
- [ ] Include all states (hover, active, focus, disabled, error)

### ✅ Documentation Phase
- [ ] Add "Styling & Theming" section to component SKILL.md
- [ ] List all component-specific tokens used
- [ ] Provide custom theming example
- [ ] Reference `design-tokens/` skill for complete documentation

### ✅ Testing Phase
- [ ] Test with light theme
- [ ] Test with dark theme
- [ ] Test with high-contrast theme
- [ ] Test in RTL mode (`<html dir="rtl">`)
- [ ] Verify no hardcoded values
- [ ] Verify theme switching works

---

## Examples

### Example 1: Button Component (forms skill)

**Component Tokens (design-tokens/tokens/components/button.json):**

```json
{
  "button": {
    "bg": {
      "primary": {
        "$value": "{semantic.color.primary}",
        "$type": "color",
        "$description": "Background color for primary buttons"
      },
      "primary-hover": {
        "$value": "{semantic.color.primary-hover}",
        "$type": "color"
      },
      "secondary": {
        "$value": "{semantic.color.secondary}",
        "$type": "color"
      },
      "disabled": {
        "$value": "{semantic.color.disabled}",
        "$type": "color"
      }
    },
    "text": {
      "primary": {
        "$value": "{semantic.color.text-inverse}",
        "$type": "color"
      }
    },
    "padding": {
      "inline": {
        "$value": "{semantic.spacing.lg}",
        "$type": "dimension"
      },
      "block": {
        "$value": "{semantic.spacing.sm}",
        "$type": "dimension"
      }
    },
    "border-radius": {
      "$value": "{semantic.radius.md}",
      "$type": "dimension"
    },
    "font-size": {
      "$value": "{semantic.font-size.base}",
      "$type": "fontSize"
    }
  }
}
```

**Component Implementation:**

```tsx
// Button.tsx
export function Button({ variant = 'primary', children, ...props }) {
  return (
    <button
      className="btn"
      data-variant={variant}
      {...props}
    >
      {children}
    </button>
  );
}
```

```css
/* Button.module.css */
.btn {
  background-color: var(--button-bg-primary);
  color: var(--button-text-primary);
  padding-inline: var(--button-padding-inline);
  padding-block: var(--button-padding-block);
  border-radius: var(--button-border-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  border: none;
  cursor: pointer;
  transition: var(--transition-fast);
}

.btn:hover {
  background-color: var(--button-bg-primary-hover);
}

.btn[data-variant="secondary"] {
  background-color: var(--button-bg-secondary);
}

.btn:disabled {
  background-color: var(--button-bg-disabled);
  cursor: not-allowed;
}
```

---

### Example 2: Chart Component (data-viz skill)

**Component Tokens:**

```json
{
  "chart": {
    "color": {
      "1": { "$value": "#648FFF", "$type": "color" },
      "2": { "$value": "#785EF0", "$type": "color" },
      "3": { "$value": "#DC267F", "$type": "color" },
      "4": { "$value": "#FE6100", "$type": "color" },
      "5": { "$value": "#FFB000", "$type": "color" }
    },
    "axis": {
      "color": { "$value": "{semantic.color.border}", "$type": "color" }
    },
    "grid": {
      "color": { "$value": "{semantic.color.border-subtle}", "$type": "color" }
    },
    "tooltip": {
      "bg": { "$value": "{semantic.color.bg-overlay}", "$type": "color" }
    },
    "font-family": {
      "$value": "{semantic.font.sans}",
      "$type": "fontFamily"
    }
  }
}
```

**Component Implementation (Recharts):**

```tsx
import { LineChart, Line, XAxis, YAxis } from 'recharts';

export function SalesChart({ data }) {
  return (
    <LineChart data={data}>
      <XAxis stroke="var(--chart-axis-color)" />
      <YAxis stroke="var(--chart-axis-color)" />
      <Line
        type="monotone"
        dataKey="sales"
        stroke="var(--chart-color-1)"
        strokeWidth={2}
      />
    </LineChart>
  );
}
```

---

## Summary

**Key Takeaways:**

1. ✅ **All component skills MUST use design tokens** for visual styling
2. ✅ **Use CSS logical properties** for RTL support (`padding-inline`, not `padding-left`)
3. ✅ **Component tokens follow naming convention**: `--{component}-{property}-{variant?}-{state?}`
4. ✅ **No hardcoded values** - everything must be tokenized
5. ✅ **Theme switching is automatic** via `data-theme` attribute
6. ✅ **W3C format required**: Use `$value`, `$type`, `$description` in token files

**This architecture enables:**
- 🎨 Automatic theming (light/dark/custom brands)
- 🌍 RTL support for international languages
- ♿ Accessibility (high-contrast themes)
- 🔄 Zero-coupling between behavior and styling
- 🚀 Infinite customization without code changes

---

**END OF SKILL CHAINING ARCHITECTURE**

*This document defines the contract between design-tokens and all component skills, ensuring consistent, themeable, and accessible UI styling across the entire component library.*
