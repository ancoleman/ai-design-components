# AI Design Components Library Context

> **Critical Reference**: This document provides the assembling-components skill with deep awareness of the AI Design Components library structure, enabling intelligent assembly that generic LLM knowledge cannot provide.

## Why This Context Matters

LLMs are already proficient at general application assembly. This skill's unique value comes from:

1. **Library-Specific Knowledge** - Understanding our exact component outputs
2. **Token System Mastery** - Knowing our precise naming conventions
3. **Skill Chain Awareness** - Understanding what each skill produces
4. **Integration Intelligence** - Knowing how our components connect

---

## Skill Chain Architecture

### Standard Skill Chain Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  theming-   │────▶│  designing- │────▶│  creating-  │
│  components │     │  layouts    │     │  dashboards │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   tokens.css         Layout.tsx         Dashboard.tsx
   globals.css        Header.tsx         KPICard.tsx
                      Sidebar.tsx
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │  visualizing-data     │
               │  (data-viz skill)     │
               └───────────────────────┘
                           │
                           ▼
                   DonutChart.tsx
                   BarChart.tsx
                   LineChart.tsx
                           │
                           ▼
               ┌───────────────────────┐
               │  providing-feedback   │
               └───────────────────────┘
                           │
                           ▼
                    Toast.tsx
                    Spinner.tsx
                    EmptyState.tsx
                           │
                           ▼
               ┌───────────────────────┐
               │ ASSEMBLING-COMPONENTS │
               │    (THIS SKILL)       │
               └───────────────────────┘
                           │
                           ▼
                 WORKING COMPONENT SYSTEM
```

### Skill Outputs Reference

| Skill | Primary Outputs | Token Dependencies |
|-------|-----------------|-------------------|
| `theming-components` | tokens.css, theme-provider.tsx | Foundation - no deps |
| `designing-layouts` | Layout.tsx, Header.tsx, grid CSS | Spacing, borders |
| `creating-dashboards` | Dashboard.tsx, grid structures | All layout tokens |
| `visualizing-data` | Chart components, legends | Colors, typography |
| `building-forms` | Form inputs, validation | Spacing, borders |
| `building-tables` | Table components, pagination | Colors, spacing |
| `providing-feedback` | Toast, Spinner, EmptyState | Colors, shadows |

---

## Token System Reference

### Token Naming Conventions

Our library uses a **semantic token architecture** with these categories:

#### Color Tokens
```css
/* Brand colors (source of truth) */
--color-cyber-orange: #FA582D;
--color-prisma-blue: #00C0E8;
--color-cortex-green: #00CC66;
--color-strata-yellow: #FFCB06;
--color-unit42-red: #C84727;

/* Semantic mappings */
--color-primary: var(--color-cyber-orange);
--color-success: var(--color-cortex-green);
--color-warning: var(--color-strata-yellow);
--color-error: var(--color-unit42-red);
--color-info: var(--color-prisma-blue);

/* Surface colors */
--color-bg-primary: #FFFFFF;      /* Main background */
--color-bg-secondary: #F8FAFC;    /* Elevated surfaces */
--color-bg-tertiary: #F1F5F9;     /* Subtle backgrounds */
--color-bg-elevated: #FFFFFF;     /* Cards, modals */

/* Text colors */
--color-text-primary: #1E293B;    /* Headings, body */
--color-text-secondary: #64748B;  /* Descriptions */
--color-text-tertiary: #94A3B8;   /* Muted text */
--color-text-inverse: #FFFFFF;    /* On dark backgrounds */
```

#### Spacing Tokens
```css
/* Base scale (4px unit) */
--space-1: 0.25rem;   /* 4px - xs */
--space-2: 0.5rem;    /* 8px - sm */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px - md */
--space-6: 1.5rem;    /* 24px - lg */
--space-8: 2rem;      /* 32px - xl */
--space-12: 3rem;     /* 48px - 2xl */

/* Semantic aliases */
--spacing-xs: var(--space-1);
--spacing-sm: var(--space-2);
--spacing-md: var(--space-4);
--spacing-lg: var(--space-6);
--spacing-xl: var(--space-8);
--spacing-2xl: var(--space-12);
```

#### Component Size Tokens
```css
/* Icons */
--icon-size-sm: 1rem;      /* 16px */
--icon-size-md: 1.5rem;    /* 24px */
--icon-size-lg: 2rem;      /* 32px */
--icon-size-xl: 3rem;      /* 48px */

/* Buttons */
--button-height-sm: 2rem;
--button-height-md: 2.5rem;
--button-height-lg: 3rem;

/* Cards/Charts */
--min-height-card: 140px;
--min-height-chart: 200px;
```

---

## Component Integration Patterns

### Import Chain (Critical Order)

```typescript
// src/main.tsx - CORRECT ORDER
import './styles/tokens.css'      // 1. Tokens first!
import './styles/globals.css'     // 2. Global resets
import './styles/components.css'  // 3. Component styles

import { ThemeProvider } from '@/context/theme-provider'
import App from './App'
```

### Component Directory Structure

```
src/components/
├── ui/                     # From theming-components, forms skills
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── index.ts           # Barrel export
├── layout/                 # From designing-layouts skill
│   ├── header.tsx
│   ├── sidebar.tsx
│   ├── footer.tsx
│   └── index.ts
├── charts/                 # From visualizing-data skill
│   ├── donut-chart.tsx
│   ├── bar-chart.tsx
│   ├── line-chart.tsx
│   └── index.ts
├── feedback/               # From providing-feedback skill
│   ├── toast.tsx
│   ├── spinner.tsx
│   ├── empty-state.tsx
│   └── index.ts
└── features/               # Domain-specific compositions
    └── dashboard/
        ├── kpi-card.tsx
        ├── dashboard.tsx
        └── index.ts
```

### State Integration Patterns

```typescript
// Theme context - always at root
<ThemeProvider>
  <App />
</ThemeProvider>

// Toast context - for notifications
<ToastProvider>
  <ThemeProvider>
    <App />
  </ThemeProvider>
</ToastProvider>
```

---

## Skill-Specific Assembly Rules

### After theming-components Skill

**Expected outputs:**
- `tokens.css` with complete token definitions
- Dark theme via `[data-theme="dark"]` selector
- Reduced motion support via `@media (prefers-reduced-motion)`

**Assembly actions:**
1. Verify tokens.css has all 7 categories (colors, spacing, typography, borders, shadows, motion, z-index)
2. Create theme-provider.tsx if not present
3. Ensure index.html has no `data-theme` attribute (let JS handle it)

### After designing-layouts Skill

**Expected outputs:**
- Layout components (Header, Sidebar, Footer)
- CSS Grid/Flexbox patterns
- Responsive breakpoints

**Assembly actions:**
1. Wire layout components into App.tsx
2. Verify layout CSS uses spacing tokens (not px values)
3. Check responsive classes use correct breakpoints

### After creating-dashboards Skill

**Expected outputs:**
- Dashboard.tsx with grid layout
- KPI cards with trend indicators
- Section organization

**Assembly actions:**
1. Import chart components from visualizing-data
2. Wire data fetching/state management
3. Ensure loading states use Spinner from feedback

### After visualizing-data Skill

**Expected outputs:**
- Chart components (Donut, Bar, Line, etc.)
- Legend components
- Accessible chart markup

**Assembly actions:**
1. Verify chart colors use `--chart-color-*` tokens
2. Check legends use correct typography tokens
3. Ensure empty states are handled

### After providing-feedback Skill

**Expected outputs:**
- Toast/notification system
- Loading spinners
- Empty states
- Error boundaries

**Assembly actions:**
1. Create ToastProvider context
2. Wire toast system to API error handlers
3. Add loading spinners to async operations

---

## Validation Checklist (Library-Specific)

### Token Compliance
- [ ] All colors use `--color-*` tokens (not hex/rgb)
- [ ] All spacing uses `--spacing-*` or `--space-*` tokens
- [ ] All typography uses `--font-size-*`, `--font-weight-*` tokens
- [ ] All radii use `--radius-*` tokens
- [ ] All shadows use `--shadow-*` tokens
- [ ] All transitions use `--transition-*` or `--duration-*` tokens
- [ ] All z-indices use `--z-*` tokens

### Theme System
- [ ] Theme toggle updates `data-theme` attribute on `<html>`
- [ ] Dark theme has all required color overrides
- [ ] System preference detection works
- [ ] Theme persists in localStorage

### Component Integration
- [ ] All component CSS imports tokens.css (or inherits)
- [ ] Barrel exports exist for each component directory
- [ ] No circular imports
- [ ] TypeScript types are exported

### Accessibility
- [ ] `prefers-reduced-motion` disables animations
- [ ] Focus states use `--color-border-focus` or `--shadow-focus`
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] Interactive elements have focus-visible styles

---

## Common Integration Patterns

### Theme Toggle Button
```typescript
// Uses our token system
function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button
      className="theme-toggle"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
    >
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>
  )
}
```

```css
.theme-toggle {
  width: var(--button-height-md);
  height: var(--button-height-md);
  background: var(--color-bg-tertiary);
  border: var(--border-width-thin) solid var(--color-border-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
}

.theme-toggle:hover {
  background: var(--color-bg-secondary);
}
```

### KPI Card with Severity
```typescript
interface KPICardProps {
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  // ...
}

function KPICard({ severity, ...props }: KPICardProps) {
  return (
    <div className={`kpi-card kpi-card--${severity}`}>
      {/* Uses severity-specific tokens */}
    </div>
  )
}
```

### Toast Notifications
```typescript
// Toast types map to our semantic colors
type ToastType = 'success' | 'error' | 'warning' | 'info'

function Toast({ type, message }: { type: ToastType; message: string }) {
  return (
    <div className={`toast toast--${type}`}>
      <div className="toast__icon">{icons[type]}</div>
      <div className="toast__content">{message}</div>
    </div>
  )
}
```

---

## Version Compatibility

| AI Design Components | React | Next.js | Python | Rust |
|---------------------|-------|---------|--------|------|
| v0.2.x | 18.x | 14.x, 15.x | 3.11+ | 1.75+ |

---

## Summary

This skill is **not** about generic app assembly - it's about understanding our specific design library's:

1. **14 component skills** and what each produces
2. **Token system** with precise naming conventions
3. **Skill chain workflow** and expected outputs at each step
4. **Integration patterns** unique to our library

The validation scripts and assembly rules encode this library-specific knowledge, ensuring consistent, token-compliant applications regardless of the target ecosystem.
