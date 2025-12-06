# React + Vite Template

> Complete scaffolding template for single-page applications using Vite and React with TypeScript.


## Table of Contents

- [Project Structure](#project-structure)
- [Core Files](#core-files)
  - [index.html](#indexhtml)
  - [package.json](#packagejson)
  - [vite.config.ts](#viteconfigts)
  - [tsconfig.json](#tsconfigjson)
  - [tsconfig.node.json](#tsconfignodejson)
  - [src/main.tsx](#srcmaintsx)
  - [src/App.tsx](#srcapptsx)
  - [src/context/theme-provider.tsx](#srccontexttheme-providertsx)
  - [src/lib/utils.ts](#srclibutilsts)
- [Barrel Export Pattern](#barrel-export-pattern)
- [Commands](#commands)
- [Integration Checklist](#integration-checklist)

## Project Structure

```
project-name/
├── index.html                 # Entry point
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
├── tsconfig.node.json         # Node-specific TypeScript config
├── vite.config.ts             # Vite configuration
├── public/
│   └── favicon.svg
└── src/
    ├── main.tsx               # React bootstrap
    ├── App.tsx                # Root component
    ├── styles/
    │   ├── tokens.css         # Design tokens (FIRST import)
    │   └── globals.css        # Global resets
    ├── context/
    │   └── theme-provider.tsx # Theme context
    ├── components/
    │   ├── ui/                # Shared UI components
    │   │   ├── button.tsx
    │   │   ├── card.tsx
    │   │   └── index.ts       # Barrel export
    │   ├── layout/            # Layout components
    │   │   ├── header.tsx
    │   │   ├── sidebar.tsx
    │   │   └── index.ts
    │   ├── charts/            # Data visualization
    │   │   ├── donut-chart.tsx
    │   │   └── index.ts
    │   ├── feedback/          # Feedback components
    │   │   ├── toast.tsx
    │   │   ├── spinner.tsx
    │   │   └── index.ts
    │   └── features/          # Feature components
    │       └── dashboard/
    │           ├── kpi-card.tsx
    │           ├── dashboard.tsx
    │           └── index.ts
    ├── hooks/
    │   └── use-theme.ts
    ├── lib/
    │   └── utils.ts
    └── types/
        └── index.ts
```

## Core Files

### index.html

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

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
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
    "vite": "^5.4.0"
  }
}
```

### vite.config.ts

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
  build: {
    sourcemap: true,
  },
})
```

### tsconfig.json

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

### tsconfig.node.json

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

### src/main.tsx

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@/context/theme-provider'
import App from './App'

// CRITICAL: Import order matters!
import './styles/tokens.css'   // 1. Design tokens FIRST
import './styles/globals.css'  // 2. Global resets

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
```

### src/App.tsx

```tsx
import { Header, Sidebar } from '@/components/layout'
import { Dashboard } from '@/components/features/dashboard'
import './App.css'

function App() {
  return (
    <div className="app">
      <Header />
      <div className="app__body">
        <Sidebar />
        <main className="app__main">
          <Dashboard />
        </main>
      </div>
    </div>
  )
}

export default App
```

### src/context/theme-provider.tsx

```tsx
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

  // Listen for system theme changes
  useEffect(() => {
    if (theme !== 'system') return

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = () => {
      const root = window.document.documentElement
      root.setAttribute('data-theme', mediaQuery.matches ? 'dark' : 'light')
    }

    mediaQuery.addEventListener('change', handleChange)
    return () => mediaQuery.removeEventListener('change', handleChange)
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

### src/lib/utils.ts

```typescript
import { type ClassValue, clsx } from 'clsx'

/**
 * Utility for conditionally joining classNames together
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}
```

## Barrel Export Pattern

Each component directory should have an index.ts file:

```typescript
// src/components/ui/index.ts
export { Button } from './button'
export { Card } from './card'
export { Input } from './input'

// src/components/layout/index.ts
export { Header } from './header'
export { Sidebar } from './sidebar'
export { Footer } from './footer'

// src/components/features/dashboard/index.ts
export { Dashboard } from './dashboard'
export { KPICard } from './kpi-card'
export { DonutChart } from './donut-chart'
```

## Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Validate CSS tokens
npm run validate:tokens

# Production build
npm run build

# Preview production build
npm run preview
```

## Integration Checklist

- [ ] `tokens.css` imported before all other styles
- [ ] ThemeProvider wraps entire app
- [ ] All CSS uses token variables (no hardcoded values)
- [ ] Barrel exports exist for each component directory
- [ ] Path aliases configured (@/)
- [ ] TypeScript strict mode enabled
- [ ] Build completes without errors
