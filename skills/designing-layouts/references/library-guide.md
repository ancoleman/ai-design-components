# Layout Framework Integration Guide

## Tailwind CSS

### Configuration with Design Tokens

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      spacing: {
        'xs': 'var(--spacing-xs)',
        'sm': 'var(--spacing-sm)',
        'md': 'var(--spacing-md)',
        'lg': 'var(--spacing-lg)',
        'xl': 'var(--spacing-xl)',
        '2xl': 'var(--spacing-2xl)',
        '3xl': 'var(--spacing-3xl)',
      },
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
      maxWidth: {
        'container': 'var(--container-max-width)',
      },
      gridTemplateColumns: {
        '12': 'repeat(12, minmax(0, 1fr))',
        'auto-fit': 'repeat(auto-fit, minmax(250px, 1fr))',
        'auto-fill': 'repeat(auto-fill, minmax(250px, 1fr))',
      },
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        background: 'var(--color-background)',
        surface: 'var(--color-surface)',
        text: 'var(--color-text)',
      }
    }
  },
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
}
```

### Tailwind Layout Patterns

```jsx
// Admin Layout with Tailwind
export function TailwindAdminLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-surface border-b">
        <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden p-2 rounded-md hover:bg-gray-100"
          >
            <span className="sr-only">Open sidebar</span>
            {/* Menu icon */}
          </button>
          <h1 className="text-xl font-semibold">Dashboard</h1>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`
          fixed inset-y-0 left-0 z-30 w-64 transform bg-surface
          lg:relative lg:translate-x-0 lg:inset-0
          transition-transform duration-300 ease-in-out
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}>
          <nav className="p-4 space-y-2">
            {/* Navigation items */}
          </nav>
        </aside>

        {/* Main content */}
        <main className="flex-1 p-4 lg:p-8">
          <div className="max-w-container mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

// Responsive Grid with Tailwind
export function TailwindGrid({ items }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 lg:gap-6">
      {items.map(item => (
        <div key={item.id} className="bg-surface rounded-lg shadow-md p-4">
          {item.content}
        </div>
      ))}
    </div>
  );
}
```

### Tailwind Container Queries

```jsx
// Container queries with Tailwind
export function ResponsiveCard({ content }) {
  return (
    <div className="@container">
      <div className="bg-surface rounded-lg shadow p-4 @md:p-6 @lg:p-8">
        <div className="@md:flex @md:items-center @md:space-x-4">
          <img
            src={content.image}
            className="w-full @md:w-32 @lg:w-48 rounded"
            alt=""
          />
          <div className="mt-4 @md:mt-0 @md:flex-1">
            <h3 className="text-lg @lg:text-xl font-semibold">
              {content.title}
            </h3>
            <p className="mt-2 text-sm @lg:text-base text-gray-600">
              {content.description}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## CSS-in-JS (styled-components / Emotion)

### Styled Components with Design Tokens

```typescript
import styled from 'styled-components';

// Theme provider setup
export const theme = {
  spacing: {
    xs: 'var(--spacing-xs)',
    sm: 'var(--spacing-sm)',
    md: 'var(--spacing-md)',
    lg: 'var(--spacing-lg)',
    xl: 'var(--spacing-xl)',
  },
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
  },
  container: {
    maxWidth: 'var(--container-max-width)',
    padding: 'var(--container-padding-x)',
  }
};

// Layout components
const Container = styled.div`
  max-width: ${props => props.theme.container.maxWidth};
  margin: 0 auto;
  padding: 0 ${props => props.theme.container.padding};

  @media (min-width: ${props => props.theme.breakpoints.md}) {
    padding: 0 ${props => props.theme.spacing.lg};
  }
`;

const Grid = styled.div<{ columns?: number; gap?: string }>`
  display: grid;
  grid-template-columns: repeat(${props => props.columns || 12}, 1fr);
  gap: ${props => props.gap || props.theme.spacing.md};

  @media (max-width: ${props => props.theme.breakpoints.md}) {
    grid-template-columns: 1fr;
  }
`;

const FlexContainer = styled.div<{ direction?: string; gap?: string }>`
  display: flex;
  flex-direction: ${props => props.direction || 'row'};
  gap: ${props => props.gap || props.theme.spacing.md};

  @media (max-width: ${props => props.theme.breakpoints.sm}) {
    flex-direction: column;
  }
`;

// Responsive sidebar layout
const LayoutWrapper = styled.div`
  display: flex;
  min-height: 100vh;
`;

const Sidebar = styled.aside<{ isOpen: boolean }>`
  width: var(--sidebar-width);
  background: var(--color-surface);
  transition: transform 0.3s ease;

  @media (max-width: ${props => props.theme.breakpoints.lg}) {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 30;
    transform: translateX(${props => props.isOpen ? '0' : '-100%'});
  }
`;

const MainContent = styled.main`
  flex: 1;
  padding: ${props => props.theme.spacing.lg};

  @media (max-width: ${props => props.theme.breakpoints.md}) {
    padding: ${props => props.theme.spacing.md};
  }
`;
```

### Emotion with TypeScript

```typescript
import { css } from '@emotion/react';
import styled from '@emotion/styled';

// Type-safe theme
interface Theme {
  spacing: Record<'xs' | 'sm' | 'md' | 'lg' | 'xl', string>;
  breakpoints: Record<'sm' | 'md' | 'lg' | 'xl', string>;
}

// Media query helper
const mq = (breakpoint: keyof Theme['breakpoints']) =>
  `@media (min-width: ${theme.breakpoints[breakpoint]})`;

// Layout styles
const containerStyles = css`
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-md);

  ${mq('md')} {
    padding: 0 var(--spacing-lg);
  }
`;

// Grid with container queries
const ResponsiveGrid = styled.div`
  container-type: inline-size;

  .grid {
    display: grid;
    gap: var(--grid-gap);
    grid-template-columns: 1fr;
  }

  @container (min-width: 400px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @container (min-width: 800px) {
    .grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
`;
```

## CSS Modules

### Layout Module

```css
/* Layout.module.css */
.container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding-x);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--grid-gap);
}

.flexRow {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.sidebar {
  width: var(--sidebar-width);
  transition: width 0.3s ease;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    transform: translateX(-100%);
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .flexRow {
    flex-direction: column;
  }
}
```

```typescript
// Layout.tsx
import styles from './Layout.module.css';
import { clsx } from 'clsx';

interface LayoutProps {
  variant?: 'sidebar' | 'centered' | 'full';
  sidebarOpen?: boolean;
  children: React.ReactNode;
}

export function Layout({ variant = 'centered', sidebarOpen, children }: LayoutProps) {
  return (
    <div className={styles.container}>
      {variant === 'sidebar' && (
        <aside className={clsx(
          styles.sidebar,
          sidebarOpen && styles.open
        )}>
          {/* Sidebar content */}
        </aside>
      )}
      <main className={styles.main}>
        {children}
      </main>
    </div>
  );
}
```

## Bootstrap Integration

### Custom Bootstrap with CSS Variables

```scss
// custom-bootstrap.scss
// Override Bootstrap variables with CSS custom properties
$primary: var(--color-primary);
$secondary: var(--color-secondary);
$body-bg: var(--color-background);
$body-color: var(--color-text);

// Spacing
$spacer: 1rem;
$spacers: (
  0: 0,
  1: var(--spacing-xs),
  2: var(--spacing-sm),
  3: var(--spacing-md),
  4: var(--spacing-lg),
  5: var(--spacing-xl),
);

// Grid breakpoints
$grid-breakpoints: (
  xs: 0,
  sm: 640px,
  md: 768px,
  lg: 1024px,
  xl: 1280px,
  xxl: 1536px
);

// Container max-widths
$container-max-widths: (
  sm: 640px,
  md: 768px,
  lg: 1024px,
  xl: 1280px,
  xxl: 1536px
);

@import '~bootstrap/scss/bootstrap';

// Custom utilities
.container-fluid-responsive {
  @include make-container();

  @include media-breakpoint-up(lg) {
    max-width: var(--container-max-width);
  }
}
```

## Performance Optimization

### Critical CSS

```javascript
// Extract critical CSS for above-the-fold content
import { extractCritical } from '@emotion/server';

export function extractCriticalCSS(html) {
  const { css, ids } = extractCritical(html);

  return {
    css: css,
    // Include only layout-critical styles
    criticalStyles: `
      .container { max-width: var(--container-max-width); margin: 0 auto; }
      .grid { display: grid; gap: var(--grid-gap); }
      .flex { display: flex; }
      @media (max-width: 768px) {
        .grid { grid-template-columns: 1fr; }
        .flex { flex-direction: column; }
      }
    `,
    ids
  };
}
```

### Lazy Loading Layout Components

```typescript
import { lazy, Suspense } from 'react';

// Lazy load heavy layout components
const MasonryLayout = lazy(() => import('./MasonryLayout'));
const ComplexGrid = lazy(() => import('./ComplexGrid'));

export function LazyLayout({ type, ...props }) {
  const LayoutSkeleton = () => (
    <div className="skeleton-layout" style={{ minHeight: '400px' }} />
  );

  return (
    <Suspense fallback={<LayoutSkeleton />}>
      {type === 'masonry' && <MasonryLayout {...props} />}
      {type === 'complex' && <ComplexGrid {...props} />}
    </Suspense>
  );
}
```