# Color System

Complete color token reference for the design system.

## Color Scale Structure

Each color has a 9-shade scale from lightest (50) to darkest (900):

```css
/* Blue Scale */
--color-blue-50: #EFF6FF;
--color-blue-100: #DBEAFE;
--color-blue-200: #BFDBFE;
--color-blue-300: #93C5FD;
--color-blue-400: #60A5FA;
--color-blue-500: #3B82F6;  /* Base */
--color-blue-600: #2563EB;
--color-blue-700: #1D4ED8;
--color-blue-800: #1E40AF;
--color-blue-900: #1E3A8A;

/* Gray Scale */
--color-gray-50: #F9FAFB;
--color-gray-100: #F3F4F6;
--color-gray-200: #E5E7EB;
--color-gray-300: #D1D5DB;
--color-gray-400: #9CA3AF;
--color-gray-500: #6B7280;
--color-gray-600: #4B5563;
--color-gray-700: #374151;
--color-gray-800: #1F2937;
--color-gray-900: #111827;

/* Additional Scales: red, green, yellow, purple, pink, indigo, teal, orange */
```

## Semantic Color Tokens

Map primitive colors to semantic meaning:

```css
/* Brand Colors */
--color-primary: var(--color-blue-500);
--color-primary-light: var(--color-blue-400);
--color-primary-dark: var(--color-blue-600);

--color-secondary: var(--color-purple-500);

/* Feedback Colors */
--color-success: var(--color-green-500);
--color-success-bg: var(--color-green-50);
--color-success-border: var(--color-green-200);

--color-warning: var(--color-yellow-500);
--color-warning-bg: var(--color-yellow-50);
--color-warning-border: var(--color-yellow-200);

--color-error: var(--color-red-500);
--color-error-bg: var(--color-red-50);
--color-error-border: var(--color-red-200);

--color-info: var(--color-blue-500);
--color-info-bg: var(--color-blue-50);
--color-info-border: var(--color-blue-200);

/* Text Colors */
--color-text-primary: var(--color-gray-900);
--color-text-secondary: var(--color-gray-600);
--color-text-tertiary: var(--color-gray-400);
--color-text-inverse: var(--color-white);

/* Background Colors */
--color-bg-primary: var(--color-white);
--color-bg-secondary: var(--color-gray-50);
--color-bg-tertiary: var(--color-gray-100);

/* Border Colors */
--color-border-default: var(--color-gray-200);
--color-border-hover: var(--color-gray-300);
--color-border-focus: var(--color-primary);
```

## Dark Theme Overrides

```css
:root[data-theme="dark"] {
  /* Invert the scale direction */
  --color-text-primary: var(--color-gray-50);
  --color-text-secondary: var(--color-gray-300);

  --color-bg-primary: var(--color-gray-900);
  --color-bg-secondary: var(--color-gray-800);
  --color-bg-tertiary: var(--color-gray-700);

  --color-border-default: var(--color-gray-700);
  --color-border-hover: var(--color-gray-600);

  /* Adjust primary for better contrast on dark */
  --color-primary: var(--color-blue-400);

  /* Feedback colors stay similar but adjust backgrounds */
  --color-success-bg: var(--color-green-900);
  --color-error-bg: var(--color-red-900);
}
```

## Accessibility Requirements

### Contrast Ratios

| Usage | Minimum Ratio | WCAG Level |
|-------|---------------|------------|
| Normal text | 4.5:1 | AA |
| Large text (18px+) | 3:1 | AA |
| UI components | 3:1 | AA |
| Enhanced (AAA) | 7:1 | AAA |

### Validated Combinations

These combinations meet WCAG AA:

| Background | Text | Ratio |
|------------|------|-------|
| white | gray-900 | 15.1:1 |
| white | gray-600 | 5.7:1 |
| gray-900 | white | 15.1:1 |
| blue-500 | white | 4.5:1 |

### Colorblind-Safe Considerations

Avoid relying solely on:
- Red vs Green (deuteranopia, protanopia)
- Blue vs Purple (tritanopia)

Always pair color with:
- Icons or patterns
- Text labels
- Shape differences
