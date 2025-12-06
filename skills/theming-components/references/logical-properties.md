# CSS Logical Properties Reference

**Complete guide to CSS logical properties for RTL/i18n support**


## Table of Contents

- [Why Logical Properties?](#why-logical-properties)
- [Core Concepts](#core-concepts)
- [Complete Property Mapping](#complete-property-mapping)
  - [Margin](#margin)
  - [Padding](#padding)
  - [Borders](#borders)
  - [Positioning](#positioning)
  - [Text Alignment](#text-alignment)
  - [Sizing](#sizing)
- [Token Examples](#token-examples)
  - [✅ CORRECT - Logical Properties](#correct-logical-properties)
  - [❌ WRONG - Physical Properties](#wrong-physical-properties)
- [Browser Support](#browser-support)
- [Testing RTL](#testing-rtl)
  - [Set Document Direction](#set-document-direction)
  - [Visual Testing Checklist](#visual-testing-checklist)
  - [Browser DevTools](#browser-devtools)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Card with Start Border](#pattern-1-card-with-start-border)
  - [Pattern 2: Icon Before Text](#pattern-2-icon-before-text)
  - [Pattern 3: Dropdown Menu](#pattern-3-dropdown-menu)
- [Resources](#resources)

---

## Why Logical Properties?

**Traditional approach (broken in RTL):**
```css
.button {
  margin-left: 16px;   /* ❌ Always left, even in RTL */
  padding-right: 24px; /* ❌ Always right, even in RTL */
}
```

**Modern approach (RTL-aware):**
```css
.button {
  margin-inline-start: 16px;  /* ✅ Left in LTR, right in RTL */
  padding-inline-end: 24px;   /* ✅ Right in LTR, left in RTL */
}
```

---

## Core Concepts

**Inline Axis** = Direction of text flow
- LTR (English): Horizontal (left → right)
- RTL (Arabic): Horizontal (right → left)
- Vertical (Japanese): Vertical (top → bottom)

**Block Axis** = Direction of block stacking
- Horizontal languages: Vertical (top → bottom)

**Start** = Beginning of flow (left in LTR, right in RTL)
**End** = End of flow (right in LTR, left in RTL)

---

## Complete Property Mapping

### Margin

| Physical | Logical | Auto-Flips? |
|----------|---------|-------------|
| `margin-left` | `margin-inline-start` | ✅ Yes |
| `margin-right` | `margin-inline-end` | ✅ Yes |
| `margin-top` | `margin-block-start` | ❌ No |
| `margin-bottom` | `margin-block-end` | ❌ No |

**Shorthands:**
```css
margin-inline: 16px;        /* Both start and end */
margin-inline: 8px 16px;    /* Start, end */
margin-block: 12px;         /* Both start and end */
```

### Padding

| Physical | Logical | Auto-Flips? |
|----------|---------|-------------|
| `padding-left` | `padding-inline-start` | ✅ Yes |
| `padding-right` | `padding-inline-end` | ✅ Yes |
| `padding-top` | `padding-block-start` | ❌ No |
| `padding-bottom` | `padding-block-end` | ❌ No |

**Shorthands:**
```css
padding-inline: 24px;       /* Both start and end */
padding-block: 12px;        /* Both start and end */
```

### Borders

| Physical | Logical | Auto-Flips? |
|----------|---------|-------------|
| `border-left` | `border-inline-start` | ✅ Yes |
| `border-right` | `border-inline-end` | ✅ Yes |
| `border-top` | `border-block-start` | ❌ No |
| `border-bottom` | `border-block-end` | ❌ No |

**Properties:**
```css
border-inline-start: 1px solid #ccc;
border-inline-end-color: red;
border-inline-end-width: 2px;
border-inline-start-style: dashed;
```

### Positioning

| Physical | Logical | Auto-Flips? |
|----------|---------|-------------|
| `left` | `inset-inline-start` | ✅ Yes |
| `right` | `inset-inline-end` | ✅ Yes |
| `top` | `inset-block-start` | ❌ No |
| `bottom` | `inset-block-end` | ❌ No |

**Usage:**
```css
.dropdown {
  position: absolute;
  inset-inline-start: 0;  /* Left in LTR, right in RTL */
  inset-block-start: 100%; /* Below element */
}
```

### Text Alignment

| Physical | Logical | Auto-Flips? |
|----------|---------|-------------|
| `text-align: left` | `text-align: start` | ✅ Yes |
| `text-align: right` | `text-align: end` | ✅ Yes |
| `text-align: center` | `text-align: center` | ❌ No (same) |

### Sizing

| Physical | Logical |
|----------|---------|
| `width` | `inline-size` |
| `height` | `block-size` |
| `min-width` | `min-inline-size` |
| `max-width` | `max-inline-size` |

**Example:**
```css
.container {
  inline-size: 100%;      /* Width in horizontal, height in vertical */
  max-inline-size: 1200px;
  block-size: auto;       /* Height in horizontal */
}
```

---

## Token Examples

### ✅ CORRECT - Logical Properties

```css
:root {
  /* Spacing - inline/block */
  --button-padding-inline: 24px;
  --button-padding-block: 12px;
  --card-margin-inline-start: 16px;
  --icon-margin-inline-end: 4px;

  /* Borders - inline/block */
  --alert-border-inline-start-width: 4px;

  /* Positioning - inset */
  --dropdown-inset-inline-start: 0;
  --tooltip-inset-block-start: 100%;
}

/* Usage */
.button {
  padding-inline: var(--button-padding-inline);
  padding-block: var(--button-padding-block);
  margin-inline-start: var(--card-margin-inline-start);
}
```

### ❌ WRONG - Physical Properties

```css
:root {
  /* ❌ Don't use physical directions */
  --button-padding-left: 24px;
  --button-padding-right: 24px;
  --card-margin-left: 16px;
  --icon-margin-right: 4px;
}
```

---

## Browser Support

**Excellent support (2025):**
- Chrome/Edge: Since version 69 (2018)
- Firefox: Since version 41 (2015)
- Safari: Since version 12.1 (2019)

**Coverage:** >95% of global users

**Fallback (if needed for very old browsers):**
```css
/* Fallback */
margin-left: 16px;

/* Modern (overrides) */
margin-inline-start: 16px;
```

---

## Testing RTL

### Set Document Direction

```html
<!-- LTR (default) -->
<html dir="ltr" lang="en">

<!-- RTL (Arabic, Hebrew) -->
<html dir="rtl" lang="ar">
```

### Visual Testing Checklist

When switching to RTL, verify:
- [ ] Text alignment flips (left → right)
- [ ] Padding/margins flip
- [ ] Borders flip (left border → right border)
- [ ] Icons flip position
- [ ] Navigation order reverses
- [ ] Forms align correctly
- [ ] Tooltips position correctly

### Browser DevTools

**Chrome:**
1. Open DevTools
2. Elements panel
3. Edit `<html>` tag
4. Change `dir="ltr"` to `dir="rtl"`

**Firefox:**
1. Right-click page
2. Inspect Element
3. Edit HTML attribute

---

## Common Patterns

### Pattern 1: Card with Start Border

```css
.card {
  border-inline-start: 4px solid var(--color-primary);
  padding-inline: var(--spacing-md);
  padding-block: var(--spacing-sm);
}

/* LTR: Left border, padding-left/right */
/* RTL: Right border, padding-right/left */
```

### Pattern 2: Icon Before Text

```css
.button-icon {
  margin-inline-end: var(--spacing-xs);
}

/* LTR: Icon on left, margin-right */
/* RTL: Icon on right, margin-left */
```

### Pattern 3: Dropdown Menu

```css
.dropdown {
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: 100%;
}

/* LTR: Aligns to left edge */
/* RTL: Aligns to right edge */
```

---

## Resources

- **W3C Spec:** https://www.w3.org/TR/css-logical-1/
- **MDN Guide:** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
- **Can I Use:** https://caniuse.com/css-logical-props

---

**Always use logical properties in design tokens for automatic RTL support!**
