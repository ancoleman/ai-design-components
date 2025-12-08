# Theming Integration Requirements

**Every generated component MUST follow these theming rules.**

---

## 1. Token File Structure

When generating code, ALWAYS create these files in this order:

```
project-name/
├── tokens.css           # FIRST: All design tokens
├── index.html           # Entry point, links tokens.css
├── main.tsx             # App bootstrap, imports tokens.css
├── App.tsx or Dashboard.tsx
├── [Component].tsx      # Each component
└── [Component].css      # Component styles using tokens
```

---

## 2. Token Import Chain

**index.html must include:**
```html
<link rel="stylesheet" href="./tokens.css" />
```

**OR main.tsx must include:**
```tsx
import './tokens.css';
```

---

## 3. Component CSS Rules

**EVERY component CSS file MUST:**

### 3.1 Use ONLY CSS Variables for Colors

Never hardcode hex values:

```css
/* ✅ CORRECT */
.button { background: var(--color-primary); }

/* ❌ WRONG */
.button { background: #3B82F6; }
```

### 3.2 Use ONLY CSS Variables for Spacing

Never hardcode px values:

```css
/* ✅ CORRECT */
.card { padding: var(--spacing-md); gap: var(--spacing-sm); }

/* ❌ WRONG */
.card { padding: 16px; gap: 8px; }
```

### 3.3 Use ONLY CSS Variables for Typography

```css
/* ✅ CORRECT */
.title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-sans);
}

/* ❌ WRONG */
.title { font-size: 20px; font-weight: 600; }
```

### 3.4 Use ONLY CSS Variables for Shadows, Borders, Radii

```css
/* ✅ CORRECT */
.card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: var(--border-width-thin) solid var(--color-border-primary);
}
```

### 3.5 Use ONLY CSS Variables for Transitions

```css
/* ✅ CORRECT */
.button { transition: var(--transition-fast); }

/* ❌ WRONG */
.button { transition: all 150ms ease; }
```

---

## 4. Required Token Categories

Every tokens.css MUST define these categories:

```css
:root {
  /* 1. COLORS - Brand + Semantic + Component */
  --color-primary: #...;
  --color-bg-primary: #...;
  --color-text-primary: #...;
  --color-border-primary: #...;

  /* 2. SPACING - 4px or 8px base scale */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* 3. TYPOGRAPHY */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-normal: 400;
  --font-weight-semibold: 600;

  /* 4. BORDERS & RADIUS */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --border-width-thin: 1px;

  /* 5. SHADOWS */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);

  /* 6. MOTION */
  --duration-fast: 150ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --transition-fast: all var(--duration-fast) var(--ease-out);

  /* 7. Z-INDEX */
  --z-dropdown: 1000;
  --z-modal: 1050;
  --z-toast: 1080;
}

/* DARK THEME - Override semantic tokens */
[data-theme="dark"] {
  --color-bg-primary: #0F172A;
  --color-text-primary: #F8FAFC;
  /* ... all semantic color overrides */
}
```

---

## 5. Component Token Mapping

Each component type has specific tokens to use:

| Component | Required Tokens |
|-----------|-----------------|
| **Cards/Containers** | `--color-bg-*`, `--radius-*`, `--shadow-*`, `--spacing-*` |
| **Buttons** | `--color-primary`, `--radius-*`, `--font-weight-*`, `--transition-*` |
| **Text** | `--color-text-*`, `--font-size-*`, `--font-weight-*`, `--line-height-*` |
| **Inputs** | `--color-border-*`, `--color-bg-*`, `--radius-*`, `--spacing-*` |
| **Charts** | `--chart-color-1` through `--chart-color-6`, `--color-text-*` |
| **Toasts** | `--color-success`, `--color-error`, `--shadow-lg`, `--z-toast` |
| **Modals** | `--z-modal`, `--shadow-xl`, `--color-bg-*`, `--radius-*` |

---

## 6. Validation Checklist

Before completing code generation, verify:

- [ ] `tokens.css` exists and is imported first
- [ ] No hardcoded color values in any CSS file
- [ ] No hardcoded spacing values (px/rem) in any CSS file
- [ ] All components reference CSS variables
- [ ] Dark theme tokens are defined
- [ ] `[data-theme="dark"]` overrides exist for all semantic colors
- [ ] Theme toggle functionality works
- [ ] Reduced motion media query included

---

## 7. Theme Toggle Implementation

Always include a working theme toggle:

```tsx
function ThemeToggle() {
  const [theme, setTheme] = useState(() =>
    localStorage.getItem('theme') || 'light'
  );

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

---

## 8. Accessibility Token Requirements

Always include:

```css
/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --transition-fast: none;
    --transition-normal: none;
  }
}

/* Focus states */
:root {
  --shadow-focus: 0 0 0 3px rgba(var(--color-primary-rgb), 0.3);
}

.interactive-element:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## Summary

**Token-first approach:**
1. Generate tokens.css FIRST
2. Import in index.html OR main.tsx
3. ALL component styles use CSS variables
4. Support light AND dark themes
5. Include accessibility tokens
6. Validate before completion
