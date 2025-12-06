# Spacing System

Complete spacing token reference for the design system.


## Table of Contents

- [Base Scale](#base-scale)
- [Semantic Spacing](#semantic-spacing)
- [Component Spacing](#component-spacing)
  - [Buttons](#buttons)
  - [Form Inputs](#form-inputs)
  - [Cards](#cards)
  - [Layout](#layout)
- [Logical Properties](#logical-properties)
- [Usage Guidelines](#usage-guidelines)
  - [Consistent Rhythm](#consistent-rhythm)
  - [Touch Targets](#touch-targets)
  - [Visual Hierarchy](#visual-hierarchy)

## Base Scale

4px base unit with consistent multipliers:

```css
/* Primitive Scale */
--space-0: 0;
--space-px: 1px;
--space-0-5: 0.125rem;  /* 2px */
--space-1: 0.25rem;     /* 4px */
--space-1-5: 0.375rem;  /* 6px */
--space-2: 0.5rem;      /* 8px */
--space-2-5: 0.625rem;  /* 10px */
--space-3: 0.75rem;     /* 12px */
--space-3-5: 0.875rem;  /* 14px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-7: 1.75rem;     /* 28px */
--space-8: 2rem;        /* 32px */
--space-9: 2.25rem;     /* 36px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-14: 3.5rem;     /* 56px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
--space-24: 6rem;       /* 96px */
--space-32: 8rem;       /* 128px */
```

## Semantic Spacing

```css
/* T-shirt sizing for general use */
--spacing-xs: var(--space-1);   /* 4px */
--spacing-sm: var(--space-2);   /* 8px */
--spacing-md: var(--space-4);   /* 16px */
--spacing-lg: var(--space-6);   /* 24px */
--spacing-xl: var(--space-8);   /* 32px */
--spacing-2xl: var(--space-12); /* 48px */
--spacing-3xl: var(--space-16); /* 64px */
```

## Component Spacing

### Buttons

```css
--button-padding-xs: var(--space-1) var(--space-2);
--button-padding-sm: var(--space-1-5) var(--space-3);
--button-padding-md: var(--space-2) var(--space-4);
--button-padding-lg: var(--space-2-5) var(--space-5);
--button-padding-xl: var(--space-3) var(--space-6);

--button-gap: var(--space-2);  /* Between icon and text */
```

### Form Inputs

```css
--input-padding-x: var(--space-3);
--input-padding-y: var(--space-2);
--input-gap: var(--space-2);        /* Between label and input */
--field-gap: var(--space-4);        /* Between form fields */
```

### Cards

```css
--card-padding: var(--space-4);
--card-padding-lg: var(--space-6);
--card-gap: var(--space-3);         /* Between card elements */
```

### Layout

```css
--container-padding-x: var(--space-4);
--container-padding-x-lg: var(--space-8);

--section-gap: var(--space-16);     /* Between page sections */
--stack-gap: var(--space-4);        /* Vertical stack of elements */
--inline-gap: var(--space-2);       /* Horizontal inline elements */

--grid-gap: var(--space-4);
--grid-gap-lg: var(--space-6);
```

## Logical Properties

Use logical properties for RTL support:

```css
/* Instead of padding-left/padding-right */
padding-inline: var(--spacing-md);
padding-inline-start: var(--spacing-sm);
padding-inline-end: var(--spacing-lg);

/* Instead of padding-top/padding-bottom */
padding-block: var(--spacing-md);
padding-block-start: var(--spacing-sm);
padding-block-end: var(--spacing-lg);

/* Instead of margin-left/margin-right */
margin-inline: var(--spacing-md);
margin-inline-start: var(--spacing-sm);
margin-inline-end: var(--spacing-lg);
```

## Usage Guidelines

### Consistent Rhythm

- Use the scale consistently
- Don't use arbitrary values (e.g., 13px, 17px)
- Prefer semantic tokens over primitive values

### Touch Targets

- Minimum 44x44px for touch interfaces
- 8px minimum spacing between targets

### Visual Hierarchy

- Larger spacing = higher importance separation
- Group related items with smaller spacing
- Separate sections with larger spacing
