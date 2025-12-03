# Assembling Components - Master Plan

> **Skill Purpose**: The capstone skill that transforms component outputs from other skills into unified, production-ready component systems across React/Next.js, Python, and Rust ecosystems.

## Strategic Positioning

### The Gap This Skill Fills

Current skill chain workflow:
```
theming → layout → dashboards → data-viz → feedback → ??? → broken components
```

With this skill:
```
theming → layout → dashboards → data-viz → feedback → assembling-components → working system
```

**Problem Statement**: Individual component skills generate excellent isolated components, but nobody is responsible for:
1. Project scaffolding (entry points, config files, build systems)
2. Token integration validation (ensuring CSS uses tokens, not hardcoded values)
3. Component wiring (imports, exports, state management)
4. Cross-ecosystem consistency (same patterns across React, Python, Rust)

### Unique Value Proposition

| Capability | Why It Matters |
|------------|----------------|
| Multi-ecosystem support | One skill for React/Next.js, Python (FastAPI/Flask), Rust (Axum/Actix) |
| Token-free validation scripts | Validate CSS without consuming context tokens |
| Framework-aware scaffolding | Generate correct boilerplate for each framework |
| Integration testing | Verify components work together before delivery |

---

## Ecosystem Architecture

### 1. React/Next.js Ecosystem

#### Project Structure (2025 Best Practices)

```
project-name/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout with providers
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Global styles + token imports
│   │   └── [feature]/          # Feature-based routing
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/                 # Atomic UI components (shadcn-style)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── index.ts        # Barrel exports
│   │   ├── layout/             # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── index.ts
│   │   └── features/           # Feature-specific components
│   │       └── dashboard/
│   │           ├── kpi-card.tsx
│   │           ├── donut-chart.tsx
│   │           └── index.ts
│   ├── lib/                    # Utilities
│   │   ├── utils.ts            # cn() helper, etc.
│   │   └── constants.ts
│   ├── hooks/                  # Custom React hooks
│   │   └── use-theme.ts
│   ├── styles/                 # Design tokens
│   │   ├── tokens.css          # CSS custom properties
│   │   └── components/         # Component-specific styles
│   ├── types/                  # TypeScript definitions
│   │   └── index.ts
│   └── context/                # React Context providers
│       └── theme-provider.tsx
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── next.config.js              # or next.config.mjs
├── tailwind.config.ts          # If using Tailwind
├── postcss.config.js
└── .env.local                  # Environment variables
```

#### Framework Options

| Framework | Use Case | Key Files |
|-----------|----------|-----------|
| **Next.js 14/15** | Full-stack React apps | `next.config.js`, App Router |
| **Vite + React** | SPAs, lighter builds | `vite.config.ts`, `index.html` |
| **Remix** | Nested routing, forms | `remix.config.js`, loaders |

#### Component Library Integration Patterns

**shadcn/ui Pattern** (Recommended):
```typescript
// components/ui/button.tsx - Copy-paste approach
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background hover:bg-accent",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant, size, className }))} {...props} />
  )
}
```

**CSS Tokens Pattern** (Our approach):
```css
/* styles/tokens.css */
:root {
  --color-primary: #FA582D;
  --color-primary-hover: #B23808;
  --spacing-md: 1rem;
  --radius-md: 8px;
  /* ... */
}

[data-theme="dark"] {
  --color-bg-primary: #0F172A;
  /* ... */
}
```

```css
/* components/button.css */
.button {
  background: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
}

.button:hover {
  background: var(--color-primary-hover);
}
```

---

### 2. Python Ecosystem

#### Project Structure (FastAPI/Flask)

```
project-name/
├── src/
│   └── project_name/           # Main package
│       ├── __init__.py
│       ├── main.py             # Application entry point
│       ├── config.py           # Configuration management
│       ├── api/                # API routes
│       │   ├── __init__.py
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   ├── dashboard.py
│       │   │   └── health.py
│       │   └── dependencies.py
│       ├── core/               # Core business logic
│       │   ├── __init__.py
│       │   └── security.py
│       ├── models/             # Pydantic/SQLAlchemy models
│       │   ├── __init__.py
│       │   ├── schemas.py      # Pydantic schemas
│       │   └── database.py     # SQLAlchemy models
│       ├── services/           # Business logic services
│       │   ├── __init__.py
│       │   └── dashboard_service.py
│       ├── static/             # Static files (CSS, JS, images)
│       │   ├── css/
│       │   │   └── tokens.css
│       │   └── js/
│       └── templates/          # Jinja2 templates (if SSR)
│           ├── base.html
│           └── dashboard.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_dashboard.py
├── pyproject.toml              # Modern Python packaging
├── requirements.txt            # or requirements-dev.txt
├── .env                        # Environment variables
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

#### Framework Options

| Framework | Use Case | Key Patterns |
|-----------|----------|--------------|
| **FastAPI** | Modern APIs, async, OpenAPI | Dependency injection, Pydantic |
| **Flask** | Lightweight, flexible | Blueprints, extensions |
| **Django** | Full-featured, admin | MVT, ORM, migrations |

#### Token Integration for Python (Jinja2 Templates)

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme | default('light') }}">
<head>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/tokens.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

```python
# api/routes/dashboard.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "theme": "dark"}
    )
```

---

### 3. Rust Ecosystem

#### Project Structure (Axum/Actix)

```
project-name/
├── src/
│   ├── main.rs                 # Application entry point
│   ├── lib.rs                  # Library crate (optional)
│   ├── config.rs               # Configuration
│   ├── routes/                 # HTTP routes
│   │   ├── mod.rs
│   │   ├── dashboard.rs
│   │   └── health.rs
│   ├── handlers/               # Request handlers
│   │   ├── mod.rs
│   │   └── dashboard_handler.rs
│   ├── models/                 # Data structures
│   │   ├── mod.rs
│   │   └── dashboard.rs
│   ├── services/               # Business logic
│   │   ├── mod.rs
│   │   └── dashboard_service.rs
│   ├── middleware/             # Custom middleware
│   │   └── mod.rs
│   └── error.rs                # Error handling
├── static/                     # Static assets
│   ├── css/
│   │   └── tokens.css
│   └── js/
├── templates/                  # Tera/Askama templates
│   ├── base.html
│   └── dashboard.html
├── tests/
│   └── integration_tests.rs
├── Cargo.toml
├── Cargo.lock
├── .env
└── Dockerfile
```

#### Framework Options

| Framework | Use Case | Key Features |
|-----------|----------|--------------|
| **Axum** | Modern, tower-based | Extractors, state management |
| **Actix Web** | High performance | Actor model, middleware |
| **Rocket** | Developer-friendly | Macros, type-safe routing |

#### Module System Best Practices

```rust
// src/routes/mod.rs
pub mod dashboard;
pub mod health;

use axum::{Router, routing::get};

pub fn create_router() -> Router {
    Router::new()
        .route("/dashboard", get(dashboard::handler))
        .route("/health", get(health::handler))
}
```

```rust
// src/main.rs
mod config;
mod routes;
mod handlers;
mod models;
mod services;
mod error;

use axum::Router;
use tower_http::services::ServeDir;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .merge(routes::create_router())
        .nest_service("/static", ServeDir::new("static"));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

---

## Token Integration & Validation

### The Token Validation Problem

When components are generated by multiple skills, common issues include:
- Hardcoded pixel values instead of spacing tokens
- Hardcoded colors instead of semantic color tokens
- Missing responsive breakpoint tokens
- Inconsistent naming conventions

### Validation Rules

#### CSS Token Validation Rules

| Rule | Bad Example | Good Example |
|------|-------------|--------------|
| No hardcoded colors | `color: #FA582D` | `color: var(--color-primary)` |
| No hardcoded spacing | `padding: 16px` | `padding: var(--spacing-md)` |
| No hardcoded radii | `border-radius: 8px` | `border-radius: var(--radius-md)` |
| No hardcoded shadows | `box-shadow: 0 4px 6px...` | `box-shadow: var(--shadow-md)` |
| No hardcoded fonts | `font-size: 14px` | `font-size: var(--font-size-sm)` |
| No hardcoded transitions | `transition: all 200ms` | `transition: var(--transition-normal)` |

#### Allowed Exceptions

Some hardcoded values are acceptable:
- **Media query breakpoints**: `@media (max-width: 768px)` - breakpoints are structural
- **Outline widths**: `outline: 2px solid` - accessibility focus indicators
- **Transform values**: `transform: translateX(100%)` - animation specifics
- **SVG coordinates**: `viewBox="0 0 100 100"` - SVG internals

### Validation Script Design

```python
#!/usr/bin/env python3
"""
validate_tokens.py - CSS Design Token Validator

Scans CSS files for hardcoded values that should use design tokens.
Returns actionable fix suggestions.

ZERO CONTEXT TOKEN COST - Executed without loading into Claude's context.
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Violation:
    file: str
    line: int
    property: str
    value: str
    suggestion: str
    severity: str  # 'error' | 'warning'

# Patterns to detect hardcoded values
PATTERNS = {
    'colors': {
        'pattern': r':\s*(#[0-9A-Fa-f]{3,8}|rgb\([^)]+\)|rgba\([^)]+\))',
        'suggestion': 'Use --color-* token',
        'severity': 'error',
        'exceptions': ['currentColor', 'transparent', 'inherit']
    },
    'spacing': {
        'pattern': r'(padding|margin|gap|top|right|bottom|left):\s*(\d+)px',
        'suggestion': 'Use --spacing-* token',
        'severity': 'error',
        'exceptions': ['0px', '1px', '2px']  # Allow thin borders
    },
    'font-sizes': {
        'pattern': r'font-size:\s*(\d+)px',
        'suggestion': 'Use --font-size-* token',
        'severity': 'error'
    },
    'border-radius': {
        'pattern': r'border-radius:\s*(\d+)px',
        'suggestion': 'Use --radius-* token',
        'severity': 'warning'
    },
    'shadows': {
        'pattern': r'box-shadow:\s*\d+px\s+\d+px',
        'suggestion': 'Use --shadow-* token',
        'severity': 'warning'
    }
}

def validate_file(filepath: Path) -> List[Violation]:
    violations = []
    content = filepath.read_text()
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Skip CSS custom property definitions
        if line.strip().startswith('--'):
            continue
        # Skip comments
        if line.strip().startswith('/*') or line.strip().startswith('*'):
            continue

        for rule_name, rule in PATTERNS.items():
            matches = re.finditer(rule['pattern'], line)
            for match in matches:
                value = match.group(0)
                # Check exceptions
                if 'exceptions' in rule:
                    if any(exc in value for exc in rule['exceptions']):
                        continue

                violations.append(Violation(
                    file=str(filepath),
                    line=i,
                    property=rule_name,
                    value=value,
                    suggestion=rule['suggestion'],
                    severity=rule['severity']
                ))

    return violations

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_tokens.py <directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    css_files = list(directory.rglob('*.css'))

    all_violations = []
    for css_file in css_files:
        # Skip token definition files
        if 'tokens' in css_file.name:
            continue
        violations = validate_file(css_file)
        all_violations.extend(violations)

    if all_violations:
        print(f"\n{'='*60}")
        print(f"TOKEN VALIDATION REPORT")
        print(f"{'='*60}\n")

        errors = [v for v in all_violations if v.severity == 'error']
        warnings = [v for v in all_violations if v.severity == 'warning']

        for v in all_violations:
            icon = "❌" if v.severity == 'error' else "⚠️"
            print(f"{icon} {v.file}:{v.line}")
            print(f"   Found: {v.value}")
            print(f"   Fix: {v.suggestion}\n")

        print(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings")
        sys.exit(1 if errors else 0)
    else:
        print("✅ All CSS files use design tokens correctly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Scaffolding Templates

### React/Vite Template Files

#### package.json
```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx",
    "lint:css": "stylelint 'src/**/*.css'",
    "validate:tokens": "python scripts/validate_tokens.py src"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.4.0",
    "vite": "^5.4.0",
    "eslint": "^8.57.0",
    "stylelint": "^16.0.0"
  }
}
```

#### vite.config.ts
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  css: {
    devSourcemap: true,
  },
})
```

#### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

#### index.html
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{{PROJECT_DESCRIPTION}}" />
    <title>{{PROJECT_TITLE}}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

#### src/main.tsx
```typescript
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@/context/theme-provider'
import App from './App'
import './styles/tokens.css'
import './styles/globals.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
```

#### src/context/theme-provider.tsx
```typescript
import { createContext, useContext, useEffect, useState, ReactNode } from 'react'

type Theme = 'light' | 'dark' | 'system'

interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window !== 'undefined') {
      return (localStorage.getItem('theme') as Theme) || 'system'
    }
    return 'system'
  })

  useEffect(() => {
    const root = window.document.documentElement
    root.removeAttribute('data-theme')

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
      root.setAttribute('data-theme', systemTheme)
    } else {
      root.setAttribute('data-theme', theme)
    }

    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

---

## Integration Checklist

### Pre-Assembly Validation

Before generating the final application:

- [ ] **Token File Exists**: `tokens.css` or equivalent is present
- [ ] **Token Import Chain**: All component CSS imports tokens first
- [ ] **No Hardcoded Values**: All CSS uses token variables
- [ ] **Theme Toggle**: Dark/light mode infrastructure exists
- [ ] **Accessibility**: Reduced motion support, focus states defined

### Assembly Steps

1. **Generate Scaffolding**
   - Create project directory structure
   - Generate configuration files (package.json, tsconfig, etc.)
   - Set up build system (Vite, Next.js, Cargo, pyproject.toml)

2. **Wire Components**
   - Create barrel exports (index.ts files)
   - Generate main App component with imports
   - Set up routing (if applicable)
   - Configure state management providers

3. **Validate Integration**
   - Run token validation script
   - Check import chains are correct
   - Verify TypeScript/type checking passes
   - Test build process completes

4. **Generate Documentation**
   - README.md with setup instructions
   - Component usage examples
   - Theme customization guide

### Post-Assembly Validation

```bash
# For React/Vite
npm install
npm run validate:tokens
npm run lint
npm run build

# For Python
pip install -e .
python -m pytest
python scripts/validate_tokens.py src/static/css

# For Rust
cargo check
cargo test
cargo build --release
```

---

## Skill Structure

```
skills/assembling-applications/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── react-vite-template.md        # Full Vite+React template
│   ├── nextjs-template.md            # Next.js 14/15 template
│   ├── python-fastapi-template.md    # FastAPI template
│   ├── python-flask-template.md      # Flask template
│   ├── rust-axum-template.md         # Axum template
│   ├── rust-actix-template.md        # Actix Web template
│   ├── token-validation-rules.md     # Comprehensive validation rules
│   └── integration-patterns.md       # Cross-ecosystem patterns
├── scripts/
│   ├── validate_tokens.py            # CSS token validator (TOKEN-FREE!)
│   ├── generate_scaffold.py          # Project scaffolding generator
│   ├── check_imports.py              # Import chain validator
│   └── generate_exports.py           # Barrel export generator
├── examples/
│   ├── react-dashboard/              # Complete React example
│   ├── nextjs-dashboard/             # Complete Next.js example
│   ├── fastapi-dashboard/            # Complete FastAPI example
│   └── rust-axum-dashboard/          # Complete Rust example
└── assets/
    ├── templates/                    # Mustache/Jinja templates for scaffolding
    │   ├── react/
    │   ├── python/
    │   └── rust/
    └── schemas/
        └── project-config.json       # JSON schema for project configuration
```

---

## SKILL.md Outline

The SKILL.md file should be concise (< 500 lines) and use progressive disclosure:

```markdown
---
name: assembling-applications
description: >
  This skill transforms component outputs from other skills into
  fully functional applications. Use when you need to wire together
  components, generate project scaffolding, or validate design token
  integration across React/Next.js, Python, or Rust ecosystems.
---

## Purpose
Capstone skill for the AI Design Components skill chain. Assembles
components into working applications with proper scaffolding, token
validation, and integration testing.

## When to Use
- After running component skills (theming, layout, dashboards, etc.)
- When generating new project scaffolding
- To validate token integration across components
- To create barrel exports and wire imports

## Framework Selection

| Ecosystem | Frameworks | Reference |
|-----------|------------|-----------|
| React/TS | Vite, Next.js 14/15 | See `references/react-*.md` |
| Python | FastAPI, Flask | See `references/python-*.md` |
| Rust | Axum, Actix Web | See `references/rust-*.md` |

## Token Validation

Run validation script (executes WITHOUT loading into context):
\`\`\`bash
python scripts/validate_tokens.py <directory>
\`\`\`

See `references/token-validation-rules.md` for comprehensive rules.

## Scaffolding Generation

For framework-specific templates, reference:
- `references/react-vite-template.md`
- `references/nextjs-template.md`
- `references/python-fastapi-template.md`
- `references/rust-axum-template.md`

## Integration Checklist

Before delivery:
1. ☐ Token file exists and is imported
2. ☐ All CSS uses token variables (run validate_tokens.py)
3. ☐ Theme toggle infrastructure present
4. ☐ Build completes without errors
5. ☐ Types/linting passes
```

---

## Research Sources

### React/Next.js
- Next.js 14/15 App Router best practices (2025)
- shadcn/ui component library patterns
- Radix UI accessibility primitives
- Tailwind CSS + CSS custom properties integration

### Python
- FastAPI project structure (tiangolo patterns)
- Flask blueprints and modular design
- Pydantic v2 for validation
- Modern pyproject.toml packaging

### Rust
- Cargo workspace patterns for large projects
- Axum tower-based middleware
- Module system best practices
- Static file serving with tower-http

### Design Systems
- Style Dictionary for token transformation
- Stylelint for CSS validation automation
- CI/CD pipeline integration patterns
- Figma → Code token workflows

---

## Success Metrics

This skill is successful when:

1. **Zero Manual Fixes**: Generated applications run without manual intervention
2. **Token Compliance**: 100% of CSS uses design tokens (validated by script)
3. **Cross-Ecosystem Parity**: Same quality across React, Python, Rust
4. **Build Success Rate**: 100% of generated projects build successfully
5. **Integration Time**: < 1 minute from skill chain completion to running app

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-01 | Initial master plan created |
