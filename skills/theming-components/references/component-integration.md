# Component Integration Guide

**How component skills consume design tokens for themeable styling**


## Table of Contents

- [Quick Reference](#quick-reference)
- [Integration Pattern](#integration-pattern)
  - [Step 1: Define Component Tokens](#step-1-define-component-tokens)
  - [Step 2: Use Tokens in Component](#step-2-use-tokens-in-component)
  - [Step 3: Theme Switching Works Automatically](#step-3-theme-switching-works-automatically)
- [Complete Examples](#complete-examples)
  - [Button Component (forms skill)](#button-component-forms-skill)
  - [Chart Component (data-viz skill)](#chart-component-data-viz-skill)
- [Integration Checklist](#integration-checklist)
  - [✅ Design Phase](#design-phase)
  - [✅ Implementation Phase](#implementation-phase)
  - [✅ Documentation Phase](#documentation-phase)
  - [✅ Testing Phase](#testing-phase)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Variants](#pattern-1-variants)
  - [Pattern 2: States](#pattern-2-states)
  - [Pattern 3: Size Variants](#pattern-3-size-variants)
- [Complete Skill Documentation Template](#complete-skill-documentation-template)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
  - [❌ Hardcoded Values](#hardcoded-values)
  - [❌ Physical Properties](#physical-properties)
  - [❌ Direct Primitive References](#direct-primitive-references)
- [Resources](#resources)

This guide shows component skills how to properly use design tokens for all visual styling.

---

## Quick Reference

**Component Token Naming:**
```
--{component}-{property}-{variant?}-{state?}
```

**Examples:**
- `--button-bg-primary`
- `--button-bg-primary-hover`
- `--input-border-color-focus`
- `--chart-color-1`

---

## Integration Pattern

### Step 1: Define Component Tokens

**File:** `tokens/components/{component}.json`

```json
{
  "$schema": "https://design-tokens.org/community-group/format/1.0.0",
  "button": {
    "bg": {
      "primary": {
        "$value": "{semantic.color.primary}",
        "$type": "color"
      },
      "primary-hover": {
        "$value": "{semantic.color.primary-hover}",
        "$type": "color"
      }
    },
    "padding": {
      "inline": {
        "$value": "{semantic.spacing.lg}",
        "$type": "dimension"
      }
    }
  }
}
```

### Step 2: Use Tokens in Component

**React/TSX:**
```tsx
function Button({ variant = 'primary', children }) {
  return (
    <button
      style={{
        backgroundColor: `var(--button-bg-${variant})`,
        color: `var(--button-text-${variant})`,
        paddingInline: 'var(--button-padding-inline)',
        borderRadius: 'var(--button-border-radius)',
      }}
    >
      {children}
    </button>
  );
}
```

**CSS:**
```css
.button {
  background-color: var(--button-bg-primary);
  color: var(--button-text-primary);
  padding-inline: var(--button-padding-inline);
  padding-block: var(--button-padding-block);
  border-radius: var(--button-border-radius);
  transition: var(--transition-fast);
}

.button:hover {
  background-color: var(--button-bg-primary-hover);
}
```

### Step 3: Theme Switching Works Automatically

No code changes needed - themes override token values:

```javascript
setTheme('dark');  // All buttons become dark-themed
setTheme('brand'); // All buttons use brand colors
```

---

## Complete Examples

### Button Component (forms skill)

**Tokens** (`tokens/components/button.json`):
```json
{
  "button": {
    "bg": {
      "primary": { "$value": "{semantic.color.primary}", "$type": "color" },
      "primary-hover": { "$value": "{semantic.color.primary-hover}", "$type": "color" },
      "secondary": { "$value": "{semantic.color.bg-secondary}", "$type": "color" },
      "disabled": { "$value": "{semantic.color.disabled}", "$type": "color" }
    },
    "text": {
      "primary": { "$value": "{semantic.color.text-inverse}", "$type": "color" },
      "secondary": { "$value": "{semantic.color.text-primary}", "$type": "color" }
    },
    "padding": {
      "inline": { "$value": "{semantic.spacing.lg}", "$type": "dimension" },
      "block": { "$value": "{semantic.spacing.sm}", "$type": "dimension" }
    },
    "border-radius": { "$value": "{semantic.radius.md}", "$type": "dimension" }
  }
}
```

**Implementation:**
```css
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
  cursor: not-allowed;
}
```

---

### Chart Component (data-viz skill)

**Tokens** (`tokens/components/chart.json`):
```json
{
  "chart": {
    "color": {
      "1": { "$value": "#648FFF", "$type": "color" },
      "2": { "$value": "#785EF0", "$type": "color" },
      "3": { "$value": "#DC267F", "$type": "color" }
    },
    "axis": {
      "color": { "$value": "{semantic.color.border}", "$type": "color" }
    },
    "grid": {
      "color": { "$value": "{semantic.color.bg-tertiary}", "$type": "color" }
    },
    "tooltip": {
      "bg": { "$value": "{semantic.color.bg-inverse}", "$type": "color" }
    }
  }
}
```

**Implementation** (Recharts):
```tsx
import { LineChart, Line, XAxis, YAxis } from 'recharts';

function SalesChart({ data }) {
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

## Integration Checklist

When creating a component skill:

### ✅ Design Phase
- [ ] List all visual styling properties
- [ ] Map to token categories (color, spacing, etc.)
- [ ] Define component-specific tokens
- [ ] Use logical property names (inline/block)

### ✅ Implementation Phase
- [ ] Use CSS custom properties (`var(--token-name)`)
- [ ] Use logical properties (`padding-inline`, NOT `padding-left`)
- [ ] NO hardcoded values
- [ ] Reference component tokens (not primitives)

### ✅ Documentation Phase
- [ ] Add "Styling & Theming" section to SKILL.md
- [ ] List component tokens used
- [ ] Provide custom theming example
- [ ] Reference design-tokens skill

### ✅ Testing Phase
- [ ] Test light theme
- [ ] Test dark theme
- [ ] Test RTL mode (`<html dir="rtl">`)
- [ ] Verify theme switching works

---

## Common Patterns

### Pattern 1: Variants

```css
/* Base button */
.button {
  background-color: var(--button-bg-primary);
}

/* Variants via data attributes */
.button[data-variant="secondary"] {
  background-color: var(--button-bg-secondary);
}

.button[data-variant="danger"] {
  background-color: var(--button-bg-danger);
}
```

### Pattern 2: States

```css
.input {
  border-color: var(--input-border-color);
}

.input:hover {
  border-color: var(--input-border-color-hover);
}

.input:focus {
  border-color: var(--input-border-color-focus);
  box-shadow: var(--input-shadow-focus);
}

.input[aria-invalid="true"] {
  border-color: var(--input-border-color-error);
}
```

### Pattern 3: Size Variants

```css
.button--sm {
  height: var(--button-height-sm);
  font-size: var(--button-font-size-sm);
}

.button--md {
  height: var(--button-height-md);
  font-size: var(--button-font-size-md);
}

.button--lg {
  height: var(--button-height-lg);
  font-size: var(--button-font-size-lg);
}
```

---

## Complete Skill Documentation Template

Add this to your component skill's SKILL.md:

```markdown
## Styling & Theming

This component uses design tokens from the **design-tokens** skill for all visual styling.

### Component Tokens

See `design-tokens/tokens/components/{component}.json` for complete list.

**Primary Tokens:**
- `--{component}-bg-primary` - Primary background color
- `--{component}-text-primary` - Primary text color
- `--{component}-padding-inline` - Horizontal padding (RTL-aware)
- `--{component}-border-radius` - Corner radius

### Custom Theming

Override these tokens in your theme file:

\```css
:root[data-theme="custom"] {
  --{component}-bg-primary: #FF6B35;
  --{component}-border-radius: 20px;
}
\```

### Theme Support

- ✅ Light mode
- ✅ Dark mode
- ✅ High contrast
- ✅ Custom brand themes
- ✅ RTL languages

See `design-tokens/` skill for complete theming documentation.
```

---

## Anti-Patterns to Avoid

### ❌ Hardcoded Values

```css
/* WRONG - No theming support */
.button {
  background-color: #3B82F6;  /* ❌ Hardcoded */
  padding: 12px 24px;         /* ❌ Hardcoded */
}
```

### ❌ Physical Properties

```css
/* WRONG - Won't flip in RTL */
.button {
  padding-left: var(--button-padding);  /* ❌ Physical property */
  margin-right: 8px;                    /* ❌ Won't flip */
}
```

### ❌ Direct Primitive References

```css
/* WRONG - Skip semantic layer */
.button {
  background-color: var(--color-blue-500);  /* ❌ Use semantic tokens */
}
```

**Correct:**
```css
/* ✅ CORRECT */
.button {
  background-color: var(--button-bg-primary);  /* ✅ Component token */
  padding-inline: var(--button-padding-inline); /* ✅ Logical property */
}
```

---

## Resources

- **SKILL_CHAINING_ARCHITECTURE.md** - Complete integration architecture
- **tokens/components/** - Example component token files
- **examples/** - Working code examples
- **SKILL.md** - Main design-tokens skill documentation

---

**For complete skill chaining architecture, see:** `SKILL_CHAINING_ARCHITECTURE.md`
