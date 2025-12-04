---
sidebar_position: 15
title: Assembling Components
description: Capstone skill for wiring component outputs into production-ready systems
tags: [frontend, integration, scaffolding, assembly]
---

# Assembling Components

Transforms the outputs of AI Design Components skills into production-ready applications with validated token integration, proper import chains, and framework-specific scaffolding.

## When to Use

Use this skill when:
- Completing a skill chain workflow (theming → layout → dashboards → data-viz → feedback)
- Generating new project scaffolding for React/Vite, Next.js, FastAPI, Flask, or Rust/Axum
- Validating that all generated CSS uses design tokens (not hardcoded values)
- Creating barrel exports and wiring component imports correctly
- Assembling components from multiple skills into a unified application
- Debugging integration issues (missing entry points, broken imports, theme not switching)
- Preparing generated code for production deployment

## Overview

This skill provides library-specific context for the AI Design Components token system, component patterns, and skill chain workflow - knowledge that generic assembly patterns cannot provide. It validates token integration, generates proper scaffolding, and wires components together correctly.

## Skill Chain Context

This skill understands the output of every AI Design Components skill:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ theming-         │────▶│ designing-       │────▶│ creating-        │
│ components       │     │ layouts          │     │ dashboards       │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
    tokens.css               Layout.tsx             Dashboard.tsx
    theme-provider.tsx       Header.tsx             KPICard.tsx
        │                        │                        │
        └────────────────────────┴────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │ visualizing-data     │
                    │ providing-feedback   │
                    └──────────────────────┘
                                 │
                                 ▼
                         DonutChart.tsx
                         Toast.tsx, Spinner.tsx
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │ ASSEMBLING-          │
                    │ COMPONENTS           │
                    └──────────────────────┘
                                 │
                                 ▼
                       WORKING COMPONENT SYSTEM
```

### Expected Outputs by Skill

| Skill | Primary Outputs | Token Dependencies |
|-------|-----------------|-------------------|
| `theming-components` | tokens.css, theme-provider.tsx | Foundation |
| `designing-layouts` | Layout.tsx, Header.tsx, Sidebar.tsx | --spacing-*, --color-border-* |
| `creating-dashboards` | Dashboard.tsx, KPICard.tsx | All layout + chart tokens |
| `visualizing-data` | Chart components, legends | --chart-color-*, --font-size-* |
| `building-forms` | Form inputs, validation | --spacing-*, --radius-*, --color-error |
| `building-tables` | Table, pagination | --color-*, --spacing-* |
| `providing-feedback` | Toast, Spinner, EmptyState | --color-success/error/warning |

## Token Validation

### Run Validation Script (Token-Free Execution)

```bash
# Basic validation
python scripts/validate_tokens.py src/styles

# Strict mode with fix suggestions
python scripts/validate_tokens.py src --strict --fix-suggestions

# JSON output for CI/CD
python scripts/validate_tokens.py src --json
```

### Our Token Naming Conventions

```css
/* Colors - semantic naming */
--color-primary: #FA582D;          /* Brand primary */
--color-success: #00CC66;          /* Positive states */
--color-error: #C84727;            /* Error states */

--color-bg-primary: #FFFFFF;       /* Main background */
--color-text-primary: #1E293B;     /* Body text */

/* Spacing - 4px base unit */
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */

/* Typography */
--font-size-xs: 0.75rem;   /* 12px */
--font-size-sm: 0.875rem;  /* 14px */
--font-size-base: 1rem;    /* 16px */
```

### Validation Rules

| Must Use Tokens (Errors) | Example Fix |
|--------------------------|-------------|
| Colors | `#FA582D` → `var(--color-primary)` |
| Spacing (≥4px) | `16px` → `var(--spacing-md)` |
| Font sizes | `14px` → `var(--font-size-sm)` |

## Framework Selection

### React/TypeScript

**Choose Vite + React when:**
- Building single-page applications
- Lightweight, fast development builds
- Maximum control over configuration
- No server-side rendering needed

**Choose Next.js 14/15 when:**
- Need server-side rendering or static generation
- Building full-stack with API routes
- SEO is important
- Using React Server Components

### Python

**Choose FastAPI when:**
- Building modern async APIs
- Need automatic OpenAPI documentation
- High performance is required
- Using Pydantic for validation

**Choose Flask when:**
- Simpler, more flexible setup
- Familiar with Flask ecosystem
- Template rendering (Jinja2)
- Smaller applications

## Implementation Approach

### 1. Validate Token Integration

Before assembly, check all CSS uses tokens:

```bash
python scripts/validate_tokens.py <component-directory>
```

Fix any violations before proceeding.

### 2. Generate Project Scaffolding

**React/Vite:**
```tsx
// src/main.tsx - Entry point
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@/context/theme-provider'
import App from './App'
import './styles/tokens.css'   // FIRST - token definitions
import './styles/globals.css'  // SECOND - global resets

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
```

### 3. Wire Components Together

**Theme Provider:**
```tsx
// src/context/theme-provider.tsx
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system')

  useEffect(() => {
    const root = document.documentElement
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark' : 'light'
    root.setAttribute('data-theme', theme === 'system' ? systemTheme : theme)
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

**Barrel Exports:**
```tsx
// src/components/ui/index.ts
export { Button } from './button'
export { Card } from './card'

// src/components/features/dashboard/index.ts
export { KPICard } from './kpi-card'
export { DonutChart } from './donut-chart'
export { Dashboard } from './dashboard'
```

## Integration Checklist

Before delivery, verify:

- [ ] **Token file exists** (`tokens.css`) with all 7 categories
- [ ] **Token import order** correct (tokens.css → globals.css → components)
- [ ] **No hardcoded values** (run `validate_tokens.py`)
- [ ] **Theme toggle works** (`data-theme` attribute switches)
- [ ] **Reduced motion** supported (`@media (prefers-reduced-motion)`)
- [ ] **Build completes** without errors
- [ ] **Types pass** (TypeScript compiles)
- [ ] **Imports resolve** (no missing modules)
- [ ] **Barrel exports** exist for each component directory

## Application Assembly Workflow

1. **Validate Components**: Run `validate_tokens.py` on all generated CSS
2. **Choose Framework**: React/Vite, Next.js, FastAPI, or Rust based on requirements
3. **Generate Scaffolding**: Create project structure and configuration
4. **Wire Imports**: Set up entry point, import chain, barrel exports
5. **Add Providers**: ThemeProvider, ToastProvider at root
6. **Connect Components**: Import and compose feature components
7. **Configure Build**: vite.config, tsconfig, package.json
8. **Final Validation**: Build, type-check, lint
9. **Document**: README with setup and usage instructions

## Related Skills

- [Theming Components](./theming-components.md) - Foundation design tokens
- [Designing Layouts](./designing-layouts.md) - Layout structure
- [Creating Dashboards](./creating-dashboards.md) - Dashboard assembly
- All frontend skills - Component outputs to assemble

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/assembling-components)
- Templates: `references/react-vite-template.md`, `references/nextjs-template.md`
- Validation: `references/token-validation-rules.md`
- Context: `references/library-context.md`
- Scripts: `scripts/validate_tokens.py`, `scripts/generate_scaffold.py`
- Examples: `examples/react-dashboard/`, `examples/nextjs-dashboard/`
