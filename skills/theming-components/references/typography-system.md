# Typography System

Complete typography token reference for the design system.


## Table of Contents

- [Font Families](#font-families)
- [Type Scale](#type-scale)
- [Font Weights](#font-weights)
- [Line Heights](#line-heights)
- [Letter Spacing](#letter-spacing)
- [Semantic Typography Tokens](#semantic-typography-tokens)
  - [Headings](#headings)
  - [Body Text](#body-text)
  - [UI Text](#ui-text)
- [Accessibility Guidelines](#accessibility-guidelines)
  - [Minimum Sizes](#minimum-sizes)
  - [Readability](#readability)

## Font Families

```css
/* Primary font stack */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
             'Helvetica Neue', Arial, sans-serif;

/* Monospace for code */
--font-mono: 'Fira Code', 'JetBrains Mono', 'SF Mono', Monaco,
             'Cascadia Code', Consolas, monospace;

/* Serif for editorial/marketing (optional) */
--font-serif: 'Georgia', 'Times New Roman', serif;
```

## Type Scale

Based on 1.25 ratio (Major Third) with 16px base:

```css
/* Size Scale */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px - Base */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
--font-size-6xl: 3.75rem;   /* 60px */
```

## Font Weights

```css
--font-weight-thin: 100;
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-extrabold: 800;
--font-weight-black: 900;
```

## Line Heights

```css
--line-height-none: 1;
--line-height-tight: 1.25;
--line-height-snug: 1.375;
--line-height-normal: 1.5;      /* Default for body text */
--line-height-relaxed: 1.625;
--line-height-loose: 2;
```

## Letter Spacing

```css
--letter-spacing-tighter: -0.05em;
--letter-spacing-tight: -0.025em;
--letter-spacing-normal: 0;
--letter-spacing-wide: 0.025em;
--letter-spacing-wider: 0.05em;
--letter-spacing-widest: 0.1em;
```

## Semantic Typography Tokens

### Headings

```css
--heading-1-size: var(--font-size-4xl);
--heading-1-weight: var(--font-weight-bold);
--heading-1-line-height: var(--line-height-tight);
--heading-1-letter-spacing: var(--letter-spacing-tight);

--heading-2-size: var(--font-size-3xl);
--heading-2-weight: var(--font-weight-semibold);
--heading-2-line-height: var(--line-height-tight);

--heading-3-size: var(--font-size-2xl);
--heading-3-weight: var(--font-weight-semibold);
--heading-3-line-height: var(--line-height-snug);

--heading-4-size: var(--font-size-xl);
--heading-4-weight: var(--font-weight-medium);
--heading-4-line-height: var(--line-height-snug);
```

### Body Text

```css
--body-size: var(--font-size-base);
--body-weight: var(--font-weight-normal);
--body-line-height: var(--line-height-normal);

--body-sm-size: var(--font-size-sm);
--body-lg-size: var(--font-size-lg);
```

### UI Text

```css
--label-size: var(--font-size-sm);
--label-weight: var(--font-weight-medium);

--caption-size: var(--font-size-xs);
--caption-weight: var(--font-weight-normal);

--button-size: var(--font-size-sm);
--button-weight: var(--font-weight-medium);
```

## Accessibility Guidelines

### Minimum Sizes

- Body text: 16px minimum (14px for secondary)
- Interactive elements: 14px minimum
- Captions/labels: 12px minimum

### Readability

- Line length: 45-75 characters optimal
- Paragraph spacing: 1.5x line height
- Use relative units (rem) not pixels for scaling
