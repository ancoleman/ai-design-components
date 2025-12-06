# Theme Switching Guide

**Complete guide to implementing light/dark mode and custom brand themes**


## Table of Contents

- [How Theme Switching Works](#how-theme-switching-works)
  - [1. Define Themes with Token Overrides](#1-define-themes-with-token-overrides)
  - [2. Set Theme Attribute](#2-set-theme-attribute)
  - [3. All Components Update Automatically](#3-all-components-update-automatically)
- [Implementation Patterns](#implementation-patterns)
  - [Vanilla JavaScript](#vanilla-javascript)
  - [React Theme Provider](#react-theme-provider)
- [Creating Custom Themes](#creating-custom-themes)
  - [Brand Theme Example](#brand-theme-example)
- [System Preference Detection](#system-preference-detection)
  - [Respect User's OS Preference](#respect-users-os-preference)
- [Multi-Theme Selector](#multi-theme-selector)
- [Theme Persistence](#theme-persistence)
  - [LocalStorage (Basic)](#localstorage-basic)
  - [Cookie (Server-Side Rendering)](#cookie-server-side-rendering)
- [Avoiding Flash of Unstyled Content (FOUC)](#avoiding-flash-of-unstyled-content-fouc)
  - [Problem](#problem)
  - [Solution 1: Inline Script (Fastest)](#solution-1-inline-script-fastest)
  - [Solution 2: Server-Side Rendering](#solution-2-server-side-rendering)
- [Theme Transition Animation](#theme-transition-animation)
- [Testing Themes](#testing-themes)
  - [Manual Testing Checklist](#manual-testing-checklist)
  - [Automated Testing](#automated-testing)

---

## How Theme Switching Works

### 1. Define Themes with Token Overrides

**Light theme** (base, default):
```css
:root {
  --color-primary: #3B82F6;
  --color-background: #FFFFFF;
  --color-text-primary: #1F2937;
}
```

**Dark theme** (overrides):
```css
:root[data-theme="dark"] {
  --color-primary: #60A5FA;
  --color-background: #111827;
  --color-text-primary: #F9FAFB;
}
```

### 2. Set Theme Attribute

```javascript
document.documentElement.setAttribute('data-theme', 'dark');
```

### 3. All Components Update Automatically

No code changes needed - CSS variables cascade:

```css
.button {
  background-color: var(--button-bg-primary);
  /* Gets #3B82F6 in light, #60A5FA in dark */
}
```

---

## Implementation Patterns

### Vanilla JavaScript

```javascript
// theme-switcher.js

function setTheme(themeName) {
  // Set attribute on <html>
  document.documentElement.setAttribute('data-theme', themeName);

  // Save preference
  localStorage.setItem('theme', themeName);

  // Update UI (optional)
  updateThemeIcon(themeName);
}

function getTheme() {
  // Check saved preference
  const saved = localStorage.getItem('theme');
  if (saved) return saved;

  // Check system preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark';
  }

  return 'light'; // Default
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  setTheme(next);
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
  const theme = getTheme();
  setTheme(theme);
});

// Listen to system preference changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem('theme')) {
    setTheme(e.matches ? 'dark' : 'light');
  }
});
```

---

### React Theme Provider

```tsx
// ThemeContext.tsx
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'high-contrast' | string;

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  setTheme: () => {},
  toggleTheme: () => {},
});

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>('light');

  // Load saved theme on mount
  useEffect(() => {
    const saved = localStorage.getItem('theme');
    if (saved) {
      setThemeState(saved);
    } else {
      // Use system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setThemeState(prefersDark ? 'dark' : 'light');
    }
  }, []);

  // Apply theme when it changes
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  const toggleTheme = () => {
    setThemeState(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

**Usage:**
```tsx
// App.tsx
import { ThemeProvider } from './ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <YourApp />
    </ThemeProvider>
  );
}

// ThemeToggle.tsx
import { useTheme } from './ThemeContext';

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button onClick={toggleTheme}>
      {theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
    </button>
  );
}
```

---

## Creating Custom Themes

### Brand Theme Example

```css
/* themes/acme-brand.css */
:root[data-theme="acme"] {
  /* Brand colors */
  --color-primary: #FF6B35;      /* Acme orange */
  --color-secondary: #004E89;    /* Acme blue */
  --color-accent: #FFA62B;

  /* Brand typography */
  --font-sans: 'Poppins', sans-serif;
  --font-weight-bold: 700;

  /* Brand spacing (more generous) */
  --spacing-md: 20px;

  /* Brand borders (more rounded) */
  --radius-md: 12px;

  /* Brand shadows (softer) */
  --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.08);
}
```

**Apply theme:**
```javascript
setTheme('acme');
```

---

## System Preference Detection

### Respect User's OS Preference

```css
/* Automatically apply dark theme if user prefers */
@media (prefers-color-scheme: dark) {
  :root {
    /* Dark theme tokens */
  }
}
```

**JavaScript with manual override:**
```javascript
function getInitialTheme() {
  // 1. Check manual preference
  const saved = localStorage.getItem('theme');
  if (saved) return saved;

  // 2. Check system preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark';
  }

  // 3. Default
  return 'light';
}
```

**Listen to system changes:**
```javascript
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  // Only auto-switch if user hasn't set manual preference
  if (!localStorage.getItem('theme')) {
    setTheme(e.matches ? 'dark' : 'light');
  }
});
```

---

## Multi-Theme Selector

**Allow users to choose from multiple themes:**

```tsx
function ThemeSelector() {
  const { theme, setTheme } = useTheme();

  const themes = [
    { value: 'light', label: '☀️ Light', icon: '☀️' },
    { value: 'dark', label: '🌙 Dark', icon: '🌙' },
    { value: 'high-contrast', label: '⚡ High Contrast', icon: '⚡' },
    { value: 'acme', label: '🎨 Acme Brand', icon: '🎨' }
  ];

  return (
    <select
      value={theme}
      onChange={(e) => setTheme(e.target.value)}
      style={{
        padding: 'var(--spacing-sm)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--color-border)'
      }}
    >
      {themes.map(t => (
        <option key={t.value} value={t.value}>
          {t.label}
        </option>
      ))}
    </select>
  );
}
```

---

## Theme Persistence

### LocalStorage (Basic)

```javascript
// Save
localStorage.setItem('theme', 'dark');

// Load
const theme = localStorage.getItem('theme') || 'light';

// Clear
localStorage.removeItem('theme');
```

### Cookie (Server-Side Rendering)

```javascript
// Set cookie
document.cookie = `theme=dark; path=/; max-age=31536000`; // 1 year

// Read cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const theme = getCookie('theme') || 'light';
```

---

## Avoiding Flash of Unstyled Content (FOUC)

### Problem

Page loads with default theme, then JavaScript switches to saved theme = visual flash

### Solution 1: Inline Script (Fastest)

```html
<!DOCTYPE html>
<html>
<head>
  <script>
    // Execute BEFORE any CSS loads
    (function() {
      const theme = localStorage.getItem('theme') || 'light';
      document.documentElement.setAttribute('data-theme', theme);
    })();
  </script>
  <link rel="stylesheet" href="styles.css">
</head>
<body>...</body>
</html>
```

### Solution 2: Server-Side Rendering

```jsx
// Next.js _document.js
import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html>
      <Head />
      <body>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                const theme = localStorage.getItem('theme') || 'light';
                document.documentElement.setAttribute('data-theme', theme);
              })();
            `
          }}
        />
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

---

## Theme Transition Animation

**Smooth theme switches:**

```css
:root {
  /* Transition all color changes */
  --theme-transition: background-color 200ms ease-in-out,
                      color 200ms ease-in-out,
                      border-color 200ms ease-in-out;
}

* {
  transition: var(--theme-transition);
}

/* Disable during theme switch to prevent animation */
.theme-transitioning * {
  transition: none !important;
}
```

**JavaScript:**
```javascript
function setTheme(themeName) {
  // Add class to prevent animations
  document.documentElement.classList.add('theme-transitioning');

  // Set theme
  document.documentElement.setAttribute('data-theme', themeName);

  // Remove class after a frame
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.documentElement.classList.remove('theme-transitioning');
    });
  });

  localStorage.setItem('theme', themeName);
}
```

---

## Testing Themes

### Manual Testing Checklist

- [ ] Light theme displays correctly
- [ ] Dark theme displays correctly
- [ ] High-contrast theme meets WCAG AAA
- [ ] Custom brand themes apply correctly
- [ ] Theme persists after page reload
- [ ] System preference detection works
- [ ] No FOUC (flash of unstyled content)
- [ ] Smooth transitions between themes
- [ ] All components update correctly

### Automated Testing

```javascript
// theme.test.js
describe('Theme switching', () => {
  it('applies light theme by default', () => {
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });

  it('switches to dark theme', () => {
    setTheme('dark');
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
  });

  it('persists theme preference', () => {
    setTheme('dark');
    expect(localStorage.getItem('theme')).toBe('dark');
  });
});
```

---

**Complete theme switching implementation in:** `examples/theme-switcher.tsx`
