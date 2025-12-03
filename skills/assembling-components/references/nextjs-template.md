# Next.js 14/15 Template

> Complete scaffolding template for full-stack applications using Next.js App Router with TypeScript.

## Project Structure

```
project-name/
├── package.json
├── next.config.mjs
├── tsconfig.json
├── tailwind.config.ts         # Optional: if using Tailwind
├── postcss.config.mjs
├── .env.local
├── public/
│   ├── favicon.ico
│   └── images/
└── src/
    ├── app/
    │   ├── layout.tsx         # Root layout with providers
    │   ├── page.tsx           # Home page
    │   ├── globals.css        # Global styles + token imports
    │   ├── dashboard/
    │   │   └── page.tsx
    │   └── api/
    │       └── health/
    │           └── route.ts
    ├── components/
    │   ├── ui/
    │   │   ├── button.tsx
    │   │   ├── card.tsx
    │   │   └── index.ts
    │   ├── layout/
    │   │   ├── header.tsx
    │   │   ├── sidebar.tsx
    │   │   └── index.ts
    │   ├── charts/
    │   │   ├── donut-chart.tsx
    │   │   └── index.ts
    │   ├── feedback/
    │   │   ├── toast.tsx
    │   │   ├── spinner.tsx
    │   │   └── index.ts
    │   └── features/
    │       └── dashboard/
    │           ├── kpi-card.tsx
    │           ├── dashboard.tsx
    │           └── index.ts
    ├── lib/
    │   └── utils.ts
    ├── hooks/
    │   └── use-theme.ts
    ├── context/
    │   └── theme-provider.tsx
    ├── styles/
    │   └── tokens.css         # Design tokens
    └── types/
        └── index.ts
```

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "validate:tokens": "python scripts/validate_tokens.py src"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.4.0"
  }
}
```

### next.config.mjs

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Enable experimental features if needed
  // experimental: {
  //   serverActions: true,
  // },
}

export default nextConfig
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### src/app/layout.tsx

```tsx
import type { Metadata } from 'next'
import { ThemeProvider } from '@/context/theme-provider'

// CRITICAL: Import tokens first
import '@/styles/tokens.css'
import './globals.css'

export const metadata: Metadata = {
  title: '{{PROJECT_TITLE}}',
  description: '{{PROJECT_DESCRIPTION}}',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="data-theme"
          defaultTheme="system"
          enableSystem
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### src/app/globals.css

```css
/*
 * Global styles - tokens.css is imported in layout.tsx before this
 * All styles here should use CSS variables from tokens.css
 */

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100vh;
}

/* Focus states for accessibility */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### src/app/page.tsx

```tsx
import { Header, Sidebar } from '@/components/layout'
import { Dashboard } from '@/components/features/dashboard'

export default function Home() {
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
```

### src/context/theme-provider.tsx

```tsx
'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'

type Theme = 'light' | 'dark' | 'system'

interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

interface ThemeProviderProps {
  children: ReactNode
  attribute?: string
  defaultTheme?: Theme
  enableSystem?: boolean
}

export function ThemeProvider({
  children,
  attribute = 'data-theme',
  defaultTheme = 'system',
  enableSystem = true,
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const stored = localStorage.getItem('theme') as Theme | null
    if (stored) {
      setTheme(stored)
    }
  }, [])

  useEffect(() => {
    if (!mounted) return

    const root = window.document.documentElement

    if (theme === 'system' && enableSystem) {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
      root.setAttribute(attribute, systemTheme)
    } else {
      root.setAttribute(attribute, theme)
    }

    localStorage.setItem('theme', theme)
  }, [theme, mounted, attribute, enableSystem])

  // Prevent flash of incorrect theme
  if (!mounted) {
    return null
  }

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

### src/app/api/health/route.ts

```typescript
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
  })
}
```

## Server Components vs Client Components

### When to use Server Components (default)

- Fetching data from APIs
- Accessing backend resources directly
- Keeping sensitive information on server
- Large dependencies that should stay on server

```tsx
// app/dashboard/page.tsx (Server Component)
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

export default async function DashboardPage() {
  const data = await getData()
  return <Dashboard data={data} />
}
```

### When to use Client Components

- Interactivity (onClick, onChange, etc.)
- Browser APIs (localStorage, window, etc.)
- React hooks (useState, useEffect, useContext)
- Custom hooks that use state

```tsx
'use client'

// components/ui/button.tsx
import { useState } from 'react'

export function Button({ children, onClick }) {
  const [isLoading, setIsLoading] = useState(false)
  // ...
}
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

# Start production server
npm run start
```

## Integration Checklist

- [ ] `tokens.css` imported in layout.tsx before globals.css
- [ ] ThemeProvider wraps entire app with `'use client'`
- [ ] `suppressHydrationWarning` on html tag
- [ ] All CSS uses token variables
- [ ] Barrel exports exist for component directories
- [ ] Path aliases configured (@/)
- [ ] Server vs Client components properly separated
- [ ] Build completes without errors
