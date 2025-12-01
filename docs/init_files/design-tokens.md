# AI-Assisted Component Library: Design Tokens & Theming System
## Master Plan for Design Tokens Skill

**Document Version:** 1.0
**Date:** November 13, 2025
**Purpose:** Comprehensive design token system providing the foundational styling architecture for all component skills, enabling brand customization, theme switching, and consistent visual design

---

## Executive Summary

Design tokens are the **foundational layer** of the entire component library - the single source of truth for all visual design decisions. This skill enables:

- **Brand Agnostic Components**: Same component code works with any brand identity
- **Theme Switching**: Light/dark mode, high contrast, custom themes
- **Design Consistency**: All components reference same tokens, ensuring visual harmony
- **Platform Flexibility**: Export tokens to web, mobile, native platforms
- **Accessibility**: WCAG-compliant color combinations, reduced motion, high contrast built-in

**Critical Architectural Principle:**
```
Component Skills (Behavior + Structure)
         ↓ use
Design Tokens (Visual Styling Variables)
         ↓ organized by
Theme Files (Light, Dark, Brand-specific)
```

This separation of concerns makes the component library infinitely adaptable.

---

## Table of Contents

1. [What Are Design Tokens?](#what-are-design-tokens)
2. [Token Taxonomy](#token-taxonomy)
3. [Token Hierarchy](#token-hierarchy)
4. [Complete Token Reference](#complete-token-reference)
5. [Theme Architecture](#theme-architecture)
6. [Component Integration Patterns](#component-integration-patterns)
7. [Accessibility Considerations](#accessibility-considerations)
8. [Platform-Specific Exports](#platform-specific-exports)
9. [Tooling & Automation](#tooling--automation)
10. [Skill Structure](#skill-structure)

---

## What Are Design Tokens?

### Definition

**Design tokens** are named variables that store visual design decisions (colors, spacing, typography, etc.) in a platform-agnostic format.

**Instead of:**
```css
button {
  background-color: #3B82F6;
  padding: 16px 24px;
  border-radius: 8px;
  font-size: 16px;
}
```

**Use tokens:**
```css
button {
  background-color: var(--color-primary-500);
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
}
```

---

### Benefits

**1. Consistency**
- Single source of truth for visual design
- Changing `--color-primary` updates entire app
- No style drift between components

**2. Theming**
- Swap token values to change entire appearance
- Light/dark mode with single attribute change
- Brand customization without code changes

**3. Maintainability**
- Update design in one place
- Semantic names are self-documenting
- Easier to onboard developers/designers

**4. Scalability**
- Add new themes easily
- Platform-agnostic (works on web, iOS, Android)
- Design system evolves without breaking changes

**5. Accessibility**
- WCAG-compliant color combinations
- High contrast themes
- Reduced motion preferences
- All handled at token level

---

## Token Taxonomy

Design tokens are organized into **7 core categories**:

1. **Color Tokens** - All color values (brand, feedback, text, backgrounds, borders)
2. **Spacing Tokens** - Layout spacing, padding, margins, gaps
3. **Typography Tokens** - Fonts, sizes, weights, line heights
4. **Border & Radius Tokens** - Border widths, corner radii
5. **Shadow Tokens** - Elevation shadows, focus rings
6. **Motion Tokens** - Animation durations, easing functions
7. **Z-Index Tokens** - Layering and stacking order

---

## Token Hierarchy

Tokens are organized in **3 levels** from primitive to semantic:

### Level 1: Primitive Tokens (Foundation)

**Raw values, not used directly in components**

```css
/* Color Primitives - 9-shade palette */
--color-blue-50: #EFF6FF;
--color-blue-100: #DBEAFE;
--color-blue-200: #BFDBFE;
--color-blue-300: #93C5FD;
--color-blue-400: #60A5FA;
--color-blue-500: #3B82F6;  /* Base blue */
--color-blue-600: #2563EB;
--color-blue-700: #1D4ED8;
--color-blue-800: #1E40AF;
--color-blue-900: #1E3A8A;

/* Spacing Primitives - 4px base scale */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
```

---

### Level 2: Semantic Tokens (Purpose)

**Meaningful names based on purpose, reference primitives**

```css
/* Brand Colors */
--color-primary: var(--color-blue-500);
--color-secondary: var(--color-purple-500);
--color-accent: var(--color-orange-500);

/* Feedback Colors */
--color-success: var(--color-green-500);
--color-warning: var(--color-yellow-500);
--color-error: var(--color-red-500);
--color-info: var(--color-blue-500);

/* Text Colors */
--color-text-primary: var(--color-gray-900);
--color-text-secondary: var(--color-gray-600);
--color-text-tertiary: var(--color-gray-400);

/* Spacing Semantic */
--spacing-xs: var(--space-1);
--spacing-sm: var(--space-2);
--spacing-md: var(--space-4);
--spacing-lg: var(--space-6);
--spacing-xl: var(--space-8);
```

---

### Level 3: Component Tokens (Specific)

**Component-specific tokens, reference semantic tokens**

```css
/* Button Component Tokens */
--button-bg-primary: var(--color-primary);
--button-bg-primary-hover: var(--color-blue-600);
--button-text-primary: var(--color-white);
--button-padding-x: var(--spacing-lg);
--button-padding-y: var(--spacing-sm);
--button-border-radius: var(--radius-md);
--button-font-weight: var(--font-weight-medium);

/* Input Component Tokens */
--input-bg: var(--color-white);
--input-border-color: var(--color-gray-300);
--input-border-color-focus: var(--color-primary);
--input-text-color: var(--color-text-primary);
--input-padding-x: var(--spacing-md);
--input-height: 40px;
```

---

## Complete Token Reference

### 1. Color Tokens

#### Color Scales (Primitive)

**Generate 9-shade palette for each hue:**
- 50: Lightest (backgrounds)
- 100-400: Light shades
- 500: Base color (most saturated)
- 600-900: Dark shades

**Required Color Scales:**
```css
/* Neutrals */
--color-white: #FFFFFF;
--color-black: #000000;
--color-gray-50 through --color-gray-900

/* Brand Colors */
--color-blue-50 through --color-blue-900
--color-purple-50 through --color-purple-900
--color-orange-50 through --color-orange-900

/* Feedback Colors */
--color-green-50 through --color-green-900  /* Success */
--color-yellow-50 through --color-yellow-900 /* Warning */
--color-red-50 through --color-red-900      /* Error */
```

---

#### Semantic Color Tokens

**Brand Identity**
```css
--color-primary: var(--color-blue-500);
--color-primary-hover: var(--color-blue-600);
--color-primary-active: var(--color-blue-700);
--color-primary-light: var(--color-blue-100);

--color-secondary: var(--color-purple-500);
--color-accent: var(--color-orange-500);
```

**Feedback/Status**
```css
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
```

**Text Colors**
```css
--color-text-primary: var(--color-gray-900);    /* Body text */
--color-text-secondary: var(--color-gray-600);  /* Subdued */
--color-text-tertiary: var(--color-gray-400);   /* Placeholder */
--color-text-disabled: var(--color-gray-300);   /* Disabled */
--color-text-inverse: var(--color-white);       /* On dark bg */
--color-text-link: var(--color-primary);
--color-text-link-hover: var(--color-primary-hover);
```

**Background Colors**
```css
--color-bg-primary: var(--color-white);
--color-bg-secondary: var(--color-gray-50);
--color-bg-tertiary: var(--color-gray-100);
--color-bg-inverse: var(--color-gray-900);
--color-bg-overlay: rgba(0, 0, 0, 0.5);
```

**Border Colors**
```css
--color-border: var(--color-gray-300);
--color-border-hover: var(--color-gray-400);
--color-border-focus: var(--color-primary);
--color-border-error: var(--color-error);
```

---

### 2. Spacing Tokens

**Base Scale** (4px increments)
```css
--space-0: 0;
--space-1: 4px;    /* 0.25rem */
--space-2: 8px;    /* 0.5rem */
--space-3: 12px;   /* 0.75rem */
--space-4: 16px;   /* 1rem */
--space-5: 20px;   /* 1.25rem */
--space-6: 24px;   /* 1.5rem */
--space-8: 32px;   /* 2rem */
--space-10: 40px;  /* 2.5rem */
--space-12: 48px;  /* 3rem */
--space-16: 64px;  /* 4rem */
--space-20: 80px;  /* 5rem */
--space-24: 96px;  /* 6rem */
--space-32: 128px; /* 8rem */
```

**Semantic Spacing**
```css
--spacing-xs: var(--space-1);   /* 4px */
--spacing-sm: var(--space-2);   /* 8px */
--spacing-md: var(--space-4);   /* 16px */
--spacing-lg: var(--space-6);   /* 24px */
--spacing-xl: var(--space-8);   /* 32px */
--spacing-2xl: var(--space-12); /* 48px */
--spacing-3xl: var(--space-16); /* 64px */
```

---

### 3. Typography Tokens

**Font Families**
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Roboto', sans-serif;
--font-serif: 'Georgia', 'Times New Roman', serif;
--font-mono: 'Fira Code', 'Menlo', 'Monaco', 'Courier New', monospace;
```

**Font Sizes** (Type Scale - 1.2 ratio)
```css
--font-size-xs: 12px;   /* 0.75rem */
--font-size-sm: 14px;   /* 0.875rem */
--font-size-base: 16px; /* 1rem - base size */
--font-size-lg: 18px;   /* 1.125rem */
--font-size-xl: 20px;   /* 1.25rem */
--font-size-2xl: 24px;  /* 1.5rem */
--font-size-3xl: 30px;  /* 1.875rem */
--font-size-4xl: 36px;  /* 2.25rem */
--font-size-5xl: 48px;  /* 3rem */
--font-size-6xl: 60px;  /* 3.75rem */
--font-size-7xl: 72px;  /* 4.5rem */
```

**Font Weights**
```css
--font-weight-thin: 100;
--font-weight-extralight: 200;
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-extrabold: 800;
--font-weight-black: 900;
```

**Line Heights**
```css
--line-height-none: 1;
--line-height-tight: 1.25;
--line-height-snug: 1.375;
--line-height-normal: 1.5;
--line-height-relaxed: 1.625;
--line-height-loose: 2;
```

**Letter Spacing**
```css
--letter-spacing-tighter: -0.05em;
--letter-spacing-tight: -0.025em;
--letter-spacing-normal: 0;
--letter-spacing-wide: 0.025em;
--letter-spacing-wider: 0.05em;
--letter-spacing-widest: 0.1em;
```

---

### 4. Border & Radius Tokens

**Border Widths**
```css
--border-width-0: 0;
--border-width-thin: 1px;
--border-width-medium: 2px;
--border-width-thick: 4px;
--border-width-heavy: 8px;
```

**Border Radius**
```css
--radius-none: 0;
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-2xl: 24px;
--radius-full: 9999px; /* Pills, circles */
```

---

### 5. Shadow Tokens

**Elevation Shadows**
```css
--shadow-none: none;
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.07);
--shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.15);
--shadow-2xl: 0 24px 48px rgba(0, 0, 0, 0.2);
```

**Colored Shadows** (Focus states)
```css
--shadow-focus-primary: 0 0 0 3px rgba(59, 130, 246, 0.3);
--shadow-focus-success: 0 0 0 3px rgba(34, 197, 94, 0.3);
--shadow-focus-warning: 0 0 0 3px rgba(234, 179, 8, 0.3);
--shadow-focus-error: 0 0 0 3px rgba(239, 68, 68, 0.3);
```

**Inner Shadows**
```css
--shadow-inner-sm: inset 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-inner-md: inset 0 2px 4px rgba(0, 0, 0, 0.1);
```

---

### 6. Motion Tokens

**Durations**
```css
--duration-instant: 100ms;
--duration-fast: 150ms;
--duration-normal: 200ms;
--duration-moderate: 300ms;
--duration-slow: 500ms;
--duration-slower: 700ms;
```

**Easing Functions**
```css
--ease-linear: cubic-bezier(0, 0, 1, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

**Common Transitions**
```css
--transition-fast: all var(--duration-fast) var(--ease-out);
--transition-normal: all var(--duration-normal) var(--ease-in-out);
--transition-slow: all var(--duration-slow) var(--ease-in-out);
```

---

### 7. Z-Index Tokens

**Layering System**
```css
--z-base: 0;
--z-dropdown: 1000;
--z-sticky: 1020;
--z-fixed: 1030;
--z-modal-backdrop: 1040;
--z-modal: 1050;
--z-popover: 1060;
--z-tooltip: 1070;
--z-notification: 1080;
```

---

## Theme Architecture

### CSS Custom Properties (Recommended)

**Base Theme (Light Mode)**
```css
/* themes/light.css */
:root {
  /* Colors */
  --color-primary: #3B82F6;
  --color-background: #FFFFFF;
  --color-text-primary: #1F2937;

  /* Spacing */
  --spacing-md: 16px;

  /* Typography */
  --font-sans: 'Inter', sans-serif;
  --font-size-base: 16px;

  /* ... all tokens defined */
}
```

**Dark Theme**
```css
/* themes/dark.css */
:root[data-theme="dark"] {
  /* Override only changed tokens */
  --color-primary: #60A5FA;
  --color-background: #111827;
  --color-text-primary: #F9FAFB;
  --color-border: #374151;

  /* Shadows adjusted for dark mode */
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.5);
}
```

**Theme Switching JavaScript**
```javascript
// Set theme
function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('theme', themeName);
}

// Load saved theme on page load
const savedTheme = localStorage.getItem('theme') || 'light';
setTheme(savedTheme);

// Toggle theme
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  setTheme(next);
}
```

---

### High Contrast Theme (Accessibility)

```css
:root[data-theme="high-contrast"] {
  --color-primary: #0000FF;  /* Pure blue */
  --color-background: #FFFFFF;
  --color-text-primary: #000000;
  --color-border: #000000;

  /* Stronger shadows */
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.5);

  /* All text must have 7:1 contrast ratio */
}
```

---

### Brand Theme Example

```css
/* themes/brand-acme.css */
:root[data-theme="acme"] {
  /* Brand Colors */
  --color-primary: #FF6B35;      /* Acme Orange */
  --color-secondary: #004E89;    /* Acme Blue */

  /* Brand Typography */
  --font-sans: 'Poppins', sans-serif;
  --font-weight-normal: 400;
  --font-weight-bold: 700;

  /* Brand Spacing (more generous) */
  --spacing-md: 20px;

  /* Brand Borders (rounded) */
  --radius-md: 12px;
}
```

---

## Component Integration Patterns

### Pattern 1: Token-Aware Component

**Component uses tokens directly:**

```tsx
// Button.tsx
function Button({ variant = 'primary', children }) {
  return (
    <button
      style={{
        backgroundColor: `var(--button-bg-${variant})`,
        color: `var(--button-text-${variant})`,
        padding: `var(--button-padding-y) var(--button-padding-x)`,
        borderRadius: 'var(--button-border-radius)',
        fontSize: 'var(--button-font-size)',
        fontWeight: 'var(--button-font-weight)',
        border: 'none',
        cursor: 'pointer',
        transition: 'var(--transition-fast)',
      }}
    >
      {children}
    </button>
  );
}
```

**CSS Alternative:**
```css
/* Button.css */
.button {
  background-color: var(--button-bg-primary);
  color: var(--button-text-primary);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-border-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  transition: var(--transition-fast);
}

.button:hover {
  background-color: var(--button-bg-primary-hover);
}

.button--secondary {
  background-color: var(--button-bg-secondary);
  color: var(--button-text-secondary);
}
```

---

### Pattern 2: Theme Provider (React)

```tsx
// ThemeContext.tsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext({
  theme: 'light',
  setTheme: (theme: string) => {},
});

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

**Usage:**
```tsx
function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

---

## Accessibility Considerations

### WCAG 2.1 AA Compliance

**Color Contrast Requirements:**
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- UI components: 3:1 minimum

**Token Validation:**
```javascript
// Ensure all text/background combinations meet contrast requirements
const validateContrast = (textColor, bgColor) => {
  const contrast = calculateContrast(textColor, bgColor);
  return contrast >= 4.5; // AA standard
};
```

---

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-instant: 0ms;
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;
    --transition-fast: none;
    --transition-normal: none;
  }
}
```

---

### High Contrast Mode

```css
@media (prefers-contrast: high) {
  :root {
    /* Use high contrast token values */
    --color-primary: var(--color-blue-700);
    --color-text-primary: var(--color-black);
    --color-border: var(--color-black);
  }
}
```

---

## Platform-Specific Exports

### Style Dictionary Configuration

```json
// config.json
{
  "source": ["tokens/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [{
        "destination": "variables.css",
        "format": "css/variables"
      }]
    },
    "scss": {
      "transformGroup": "scss",
      "buildPath": "dist/scss/",
      "files": [{
        "destination": "_variables.scss",
        "format": "scss/variables"
      }]
    },
    "ios": {
      "transformGroup": "ios",
      "buildPath": "dist/ios/",
      "files": [{
        "destination": "Tokens.swift",
        "format": "ios-swift/class.swift"
      }]
    },
    "android": {
      "transformGroup": "android",
      "buildPath": "dist/android/",
      "files": [{
        "destination": "tokens.xml",
        "format": "android/resources"
      }]
    }
  }
}
```

---

## Tooling & Automation

### Token Generation

```python
# scripts/generate_theme.py
def generate_color_scale(base_color, hue_name):
    """Generate 9-shade color scale from base color"""
    shades = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    scale = {}

    for shade in shades:
        lightness = calculate_lightness(shade)
        scale[f'--color-{hue_name}-{shade}'] = adjust_color(base_color, lightness)

    return scale
```

### Token Validation

```python
# scripts/validate_tokens.py
def validate_token_structure():
    """Ensure all required tokens are defined"""
    required_categories = [
        'color', 'spacing', 'typography',
        'border', 'shadow', 'motion', 'z-index'
    ]

    for category in required_categories:
        tokens = load_tokens(category)
        validate_naming_convention(tokens)
        validate_references(tokens)
        validate_accessibility(tokens)
```

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7). This ensures you're using the latest, most secure versions.

**Note:** The recommendations below were researched comprehensively in November 2025 and are production-ready. Validation is optional.

---

## Recommended Libraries & Tools

### Industry-Standard: Style Dictionary (Amazon)

**Library:** `/amzn/style-dictionary`
**Trust Score:** 9.1/10
**Code Snippets:** 405+

**Why Style Dictionary?**
- Industry standard for design token management (used by Amazon, Adobe, others)
- Transforms tokens to ANY format (CSS, SCSS, iOS Swift, Android XML, JS, JSON)
- Platform-agnostic source of truth
- Extensible with custom transforms and formats
- Active community and enterprise-proven

**Core Workflow:**
```
JSON/JS Tokens → Style Dictionary → CSS Variables
                                  → iOS Swift
                                  → Android XML
                                  → JS/TS
                                  → SCSS
```

**Installation:**
```bash
npm install style-dictionary
```

**Basic Configuration:**
```javascript
// config.json or config.js
export default {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    },
    scss: {
      transformGroup: 'scss',
      buildPath: 'build/scss/',
      files: [{
        destination: '_variables.scss',
        format: 'scss/variables'
      }]
    },
    js: {
      transformGroup: 'js',
      buildPath: 'build/js/',
      files: [{
        destination: 'tokens.js',
        format: 'javascript/es6'
      }]
    }
  }
};
```

**Token Definition (JSON):**
```json
{
  "color": {
    "brand": {
      "primary": {
        "$value": "#3B82F6",
        "$type": "color",
        "$description": "Primary brand color"
      }
    },
    "text": {
      "primary": {
        "$value": "{color.gray.900}",
        "$type": "color"
      }
    }
  },
  "spacing": {
    "md": {
      "$value": "16px",
      "$type": "dimension"
    }
  }
}
```

**Build Command:**
```bash
style-dictionary build
```

**Output (CSS Variables):**
```css
:root {
  --color-brand-primary: #3B82F6;
  --color-text-primary: #2D3748;
  --spacing-md: 16px;
}
```

---

### Design-to-Code: Tokens Studio (Figma Plugin)

**Tool:** Tokens Studio for Figma
**Integration:** Works seamlessly with Style Dictionary via `@tokens-studio/sd-transforms`

**Workflow:**
```
Figma Design → Tokens Studio Plugin → Export JSON → Style Dictionary → Code
```

**Benefits:**
- Design tokens defined in Figma (visual interface)
- Designers control tokens directly
- Sync design and code automatically
- No manual JSON editing

**Installation:**
```bash
npm install @tokens-studio/sd-transforms
```

**Style Dictionary Configuration with Tokens Studio:**
```javascript
import StyleDictionary from 'style-dictionary';
import { registerTransforms } from '@tokens-studio/sd-transforms';

// Register Tokens Studio transforms
registerTransforms(StyleDictionary);

export default {
  source: ['tokens-studio-output/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'tokens-studio', // Use Tokens Studio transform group
      buildPath: 'build/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    }
  }
};
```

---

### Alternative: Tailwind CSS Approach

**Library:** `/tailwindlabs/tailwindcss.com`
**Trust Score:** 10/10

**For Projects Using Tailwind:**

Tailwind has built-in theming via configuration:

```javascript
// tailwind.config.js
export default {
  darkMode: 'class', // or 'media'
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
      },
      spacing: {
        '128': '32rem',
      }
    }
  }
}
```

**Usage:**
```html
<div class="bg-white dark:bg-gray-900">
  <h1 class="text-gray-900 dark:text-white">Title</h1>
</div>
```

**When to Use:**
- Already using Tailwind CSS
- Utility-first approach preferred
- Rapid prototyping
- Web-only (not multi-platform)

**When to Use Style Dictionary Instead:**
- Multi-platform (web + iOS + Android)
- Design system shared across teams
- Custom token structure needed
- Integration with design tools (Figma)

---

## Internationalization (i18n) & RTL Support

### The Challenge

Supporting multiple languages requires:
1. **RTL (Right-to-Left) Languages**: Arabic, Hebrew, Persian, Urdu
2. **Vertical Writing Modes**: Japanese, Chinese, Korean (sometimes)
3. **Text Expansion**: German text is ~30% longer than English
4. **Cultural Considerations**: Colors, icons, imagery have different meanings

**Traditional Approach (Problematic):**
```css
/* LTR styles */
.element {
  margin-left: 16px;
  padding-right: 24px;
}

/* Separate RTL stylesheet */
.element[dir="rtl"] {
  margin-left: 0;
  margin-right: 16px;
  padding-right: 0;
  padding-left: 24px;
}
```

**Problems:**
- Duplicate stylesheets
- Maintenance nightmare
- Easy to miss properties
- Doesn't scale

---

### Modern Solution: CSS Logical Properties

**CSS Logical Properties** replace physical directions with logical flow-relative directions.

**Physical → Logical Mapping:**

| Physical Property | Logical Property (LTR) | Logical Property (RTL) |
|-------------------|------------------------|------------------------|
| `margin-left` | `margin-inline-start` | `margin-inline-start` (auto-flips) |
| `margin-right` | `margin-inline-end` | `margin-inline-end` (auto-flips) |
| `margin-top` | `margin-block-start` | `margin-block-start` |
| `margin-bottom` | `margin-block-end` | `margin-block-end` |
| `padding-left` | `padding-inline-start` | (auto-flips) |
| `padding-right` | `padding-inline-end` | (auto-flips) |
| `border-left` | `border-inline-start` | (auto-flips) |
| `border-right` | `border-inline-end` | (auto-flips) |
| `text-align: left` | `text-align: start` | (auto-flips) |
| `text-align: right` | `text-align: end` | (auto-flips) |
| `left: 0` | `inset-inline-start: 0` | (auto-flips) |
| `right: 0` | `inset-inline-end: 0` | (auto-flips) |

---

### Key Concepts

**Inline Axis** = Direction of text flow
- LTR languages: Horizontal (left → right)
- RTL languages: Horizontal (right → left)
- Vertical languages: Vertical (top → bottom)

**Block Axis** = Direction of block stacking
- Horizontal languages: Vertical (top → bottom)
- Vertical languages: Horizontal (varies)

---

### Design Tokens with Logical Properties

**Instead of:**
```css
--button-padding-left: 24px;
--button-padding-right: 24px;
```

**Use:**
```css
--button-padding-inline-start: 24px;
--button-padding-inline-end: 24px;

/* Or use shorthand */
--button-padding-inline: 24px; /* Both start and end */
```

**In Components:**
```css
.button {
  padding-inline: var(--button-padding-inline);
  /* Automatically adapts:
     - LTR: padding-left and padding-right
     - RTL: padding-right and padding-left (flipped)
  */
}
```

---

### Complete Logical Property Reference

**Margin:**
```css
/* Individual sides */
margin-inline-start: 16px;  /* Left in LTR, Right in RTL */
margin-inline-end: 16px;    /* Right in LTR, Left in RTL */
margin-block-start: 8px;    /* Top */
margin-block-end: 8px;      /* Bottom */

/* Shorthands */
margin-inline: 16px;        /* Both inline sides */
margin-block: 8px;          /* Both block sides */
```

**Padding:**
```css
padding-inline-start: 24px;
padding-inline-end: 24px;
padding-block-start: 12px;
padding-block-end: 12px;

/* Shorthands */
padding-inline: 24px;
padding-block: 12px;
```

**Borders:**
```css
border-inline-start: 1px solid #ccc;
border-inline-end: 1px solid #ccc;
border-block-start: 1px solid #ccc;
border-block-end: 1px solid #ccc;

/* Shorthands */
border-inline: 1px solid #ccc;
border-block: 1px solid #ccc;
```

**Positioning:**
```css
inset-inline-start: 0;  /* left: 0 in LTR, right: 0 in RTL */
inset-inline-end: 0;    /* right: 0 in LTR, left: 0 in RTL */
inset-block-start: 0;   /* top: 0 */
inset-block-end: 0;     /* bottom: 0 */
```

**Text Alignment:**
```css
text-align: start;  /* left in LTR, right in RTL */
text-align: end;    /* right in LTR, left in RTL */
```

---

### Browser Support

**Excellent Support (2025):**
- Chrome/Edge: Since 2018
- Firefox: Since 2018
- Safari: Since 2018
- All modern browsers support logical properties

**Fallback Strategy (if supporting very old browsers):**
```css
/* Fallback for old browsers */
margin-left: 16px;

/* Modern browsers (overrides above) */
margin-inline-start: 16px;
```

Or use PostCSS plugin: `postcss-logical-properties`

---

### i18n Token Strategy

**Direction-Agnostic Tokens:**
```css
/* ✅ GOOD - Uses logical properties */
--spacing-inline-sm: 8px;
--spacing-inline-md: 16px;
--spacing-block-sm: 8px;

/* ❌ BAD - Directional, breaks in RTL */
--spacing-left: 16px;
--spacing-right: 16px;
```

**Token Naming Convention for i18n:**
```css
/* Spacing - Use inline/block, not left/right */
--space-inline-{size}
--space-block-{size}

/* Borders - Use inline/block */
--border-inline-width
--border-block-width

/* Positioning - Use inline/block */
--inset-inline-start
--inset-inline-end
```

---

### RTL Implementation Pattern

**1. Set Document Direction:**
```html
<!-- LTR (English, French, Spanish) -->
<html dir="ltr" lang="en">

<!-- RTL (Arabic, Hebrew) -->
<html dir="rtl" lang="ar">
```

**2. Use Logical Properties in Tokens:**
```css
:root {
  --button-padding-inline: 24px;
  --button-margin-inline-start: 8px;
  --icon-margin-inline-end: 4px;
}
```

**3. Components Auto-Adapt:**
```css
.button {
  padding-inline: var(--button-padding-inline);
  margin-inline-start: var(--button-margin-inline-start);
}

/* LTR: padding-left: 24px, padding-right: 24px, margin-left: 8px */
/* RTL: padding-right: 24px, padding-left: 24px, margin-right: 8px */
```

---

### Advanced: Language-Specific Token Overrides

**Some values need adjustment per language:**

```css
/* Base (English) */
:root {
  --font-family-body: 'Inter', sans-serif;
  --line-height-base: 1.5;
}

/* Arabic - needs more line height */
:root:lang(ar) {
  --font-family-body: 'Cairo', 'Inter', sans-serif;
  --line-height-base: 1.75; /* More breathing room for Arabic */
  --letter-spacing-base: 0.01em; /* Slightly more spacing */
}

/* Japanese - different font, tighter spacing */
:root:lang(ja) {
  --font-family-body: 'Noto Sans JP', sans-serif;
  --line-height-base: 1.7;
  --letter-spacing-base: 0.02em;
}

/* German - prepare for longer text */
:root:lang(de) {
  /* Use smaller font size for buttons to accommodate longer text */
  --button-font-size: var(--font-size-sm);
}
```

---

### Text Expansion Considerations

**Text length varies dramatically by language:**

| Language | Text Expansion vs. English |
|----------|----------------------------|
| German | +30% longer |
| French | +15-20% longer |
| Spanish | +20-30% longer |
| Chinese | -30% shorter |
| Japanese | -10% shorter |

**Token Strategy:**
```css
/* Don't use fixed widths */
❌ --button-width: 200px;

/* Use min-width instead */
✅ --button-min-width: 120px;
✅ --button-padding-inline: 24px; /* Let content determine width */
```

---

### Cultural Color Considerations

**Colors have different meanings across cultures:**

| Color | Western | China | Middle East |
|-------|---------|-------|-------------|
| Red | Danger, Stop | Luck, Celebration | Caution |
| White | Purity, Peace | Death, Mourning | Purity |
| Green | Success, Go | Positive | Sacred, Islam |
| Yellow | Caution | Imperial, Sacred | Happiness |
| Blue | Trust, Professional | Immortality | Protection |

**Token Strategy for Semantic Colors:**
```css
/* Define semantic intent, allow cultural overrides */
--color-success: var(--color-green-500);
--color-danger: var(--color-red-500);

/* Cultural override example (China) */
:root:lang(zh) {
  --color-success: var(--color-red-500); /* Red = positive */
  --color-danger: var(--color-yellow-500);
}
```

**Best Practice:** Use icons + color, never color alone for meaning.

---

## RTL Best Practices

### 1. Use Logical Properties Consistently

**✅ DO:**
```css
.card {
  padding-inline: var(--spacing-md);
  margin-inline-start: var(--spacing-sm);
  border-inline-start: 1px solid var(--color-border);
  text-align: start;
}
```

**❌ DON'T:**
```css
.card {
  padding-left: 16px;
  padding-right: 16px;
  margin-left: 8px;
  border-left: 1px solid #ccc;
  text-align: left;
}
```

---

### 2. Mirror Asymmetric UI Elements

**Elements that need mirroring in RTL:**
- Navigation arrows (← becomes →)
- Breadcrumb separators (/ becomes \)
- Progress bars (left-to-right becomes right-to-left)
- Carousel indicators
- Search icons (often on right in RTL)

**Using CSS:**
```css
.icon-arrow {
  /* Default (LTR): → */
  transform: rotate(0deg);
}

[dir="rtl"] .icon-arrow {
  /* RTL: ← */
  transform: rotate(180deg);
}
```

**Or use SVG with transform:**
```html
<!-- LTR -->
<svg>...</svg>

<!-- RTL: flip horizontally -->
<svg style="transform: scaleX(-1)">...</svg>
```

---

### 3. Test in Both Directions

**Testing Checklist:**
- [ ] Switch `dir` attribute: `<html dir="rtl">`
- [ ] Check all components visually
- [ ] Verify text alignment
- [ ] Check icon directions
- [ ] Test navigation flows
- [ ] Verify form layouts
- [ ] Check tooltip/popover positioning
- [ ] Test animations (should mirror)

**Browser DevTools:**
- Chrome: Can toggle `dir` attribute in Elements panel
- Firefox: Built-in text direction override

---

### 4. Automatic RTL with i18n Libraries

**react-i18next Integration:**
```jsx
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';

function App() {
  const { i18n } = useTranslation();

  useEffect(() => {
    // Set document direction based on language
    document.documentElement.dir = i18n.dir();
  }, [i18n.language]);

  return <div>...</div>;
}
```

**i18next configuration:**
```javascript
import i18next from 'i18next';

i18next.init({
  resources: {
    en: { translation: { /* ... */ } },
    ar: { translation: { /* ... */ } },
  },
  lng: 'en',
  fallbackLng: 'en',
});

// Get text direction
i18next.dir('en'); // 'ltr'
i18next.dir('ar'); // 'rtl'
```

---

### 5. Component Token Patterns for RTL

**Spacing that auto-flips:**
```css
/* These automatically reverse in RTL */
--button-icon-margin-inline-end: 8px; /* Space after icon */
--input-padding-inline-start: 12px;   /* Padding at text start */
--dropdown-arrow-inset-inline-end: 12px; /* Arrow position */
```

**Usage:**
```css
.button-icon {
  margin-inline-end: var(--button-icon-margin-inline-end);
  /* LTR: margin-right: 8px (icon on left, space on right)
     RTL: margin-left: 8px (icon on right, space on left) */
}
```

---

### 6. Symmetrical vs. Asymmetrical Spacing

**Symmetrical (same in LTR/RTL):**
```css
--card-padding: 24px; /* Uniform padding all sides */
--button-padding-block: 12px; /* Top and bottom same */
```

**Asymmetrical (context-aware):**
```css
--breadcrumb-separator-margin-inline: 8px; /* Space before/after separator */
--icon-margin-inline-end: 4px; /* Icon before text */
--checkbox-margin-inline-end: 8px; /* Checkbox before label */
```

---

## Language-Specific Token Overrides

### Font Stack per Language

```css
:root {
  --font-sans: 'Inter', system-ui, sans-serif;
}

/* Arabic */
:root:lang(ar) {
  --font-sans: 'Cairo', 'Noto Kufi Arabic', sans-serif;
  --line-height-base: 1.75; /* Arabic needs more line height */
}

/* Hebrew */
:root:lang(he) {
  --font-sans: 'Rubik', 'Noto Sans Hebrew', sans-serif;
}

/* Japanese */
:root:lang(ja) {
  --font-sans: 'Noto Sans JP', sans-serif;
  --letter-spacing-base: 0.02em;
}

/* Korean */
:root:lang(ko) {
  --font-sans: 'Noto Sans KR', sans-serif;
}

/* Chinese Simplified */
:root:lang(zh-CN) {
  --font-sans: 'Noto Sans SC', sans-serif;
}

/* Chinese Traditional */
:root:lang(zh-TW) {
  --font-sans: 'Noto Sans TC', sans-serif;
}
```

---

### Recommended i18n Token Structure

```
tokens/
├── global/
│   ├── colors.json          # Universal colors
│   ├── spacing.json         # Universal spacing (logical properties)
│   └── typography.json      # Base typography
├── themes/
│   ├── light.json
│   ├── dark.json
│   └── high-contrast.json
└── languages/
    ├── ar.json              # Arabic overrides (font, line-height)
    ├── he.json              # Hebrew overrides
    ├── ja.json              # Japanese overrides
    ├── ko.json              # Korean overrides
    └── de.json              # German overrides (spacing for longer text)
```

**Style Dictionary Config for Multi-Language:**
```javascript
export default {
  source: [
    'tokens/global/**/*.json',
    'tokens/themes/light.json'
  ],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [
        {
          destination: 'variables.css',
          format: 'css/variables'
        },
        {
          destination: 'variables-ar.css',
          source: ['tokens/global/**/*.json', 'tokens/languages/ar.json'],
          format: 'css/variables'
        },
        {
          destination: 'variables-ja.css',
          source: ['tokens/global/**/*.json', 'tokens/languages/ja.json'],
          format: 'css/variables'
        }
      ]
    }
  }
};
```

---

## Implementation Recommendations

### For This Skill: Hybrid Approach

**Use:**
1. **CSS Custom Properties** - For web implementation (fast, no build step)
2. **Style Dictionary** - For multi-platform export and build pipeline
3. **CSS Logical Properties** - For automatic RTL support
4. **Language-specific overrides** - Via `:lang()` selectors

**Workflow:**
```
1. Define tokens in JSON (Style Dictionary format)
2. Build to CSS variables (web)
3. Build to Swift/Kotlin (mobile)
4. Use logical properties in all CSS
5. Add language-specific overrides as needed
```

---

### Migration Path

**Phase 1: Core Tokens (Week 1)**
- Define primitive tokens (colors, spacing, typography)
- Build to CSS variables
- Use in components with logical properties

**Phase 2: Theme Switching (Week 2)**
- Add light/dark theme variants
- Implement theme toggle
- Test theme persistence

**Phase 3: i18n Support (Week 3)**
- Add language-specific font tokens
- Create RTL test suite
- Add language overrides

**Phase 4: Multi-Platform (Week 4)**
- Configure iOS Swift export
- Configure Android XML export
- Test on mobile platforms

---

## Skill Structure

```
design-tokens/
├── SKILL.md
│   ├── Frontmatter (name, description)
│   ├── Quick Start (using tokens in components)
│   ├── Token Categories Overview
│   └── References to detailed docs
│
├── references/
│   ├── token-taxonomy.md        # Complete token reference
│   ├── color-system.md          # Color scales, semantics, accessibility
│   ├── typography-system.md     # Type scales, fonts, readability
│   ├── spacing-system.md        # Spacing scale, layout rhythm
│   ├── theme-switching.md       # Light/dark, custom themes
│   ├── component-tokens.md      # Component-specific token patterns
│   ├── accessibility-tokens.md  # WCAG compliance, high contrast
│   ├── i18n-rtl-support.md      # Internationalization and RTL
│   ├── logical-properties.md    # CSS logical properties guide
│   ├── style-dictionary-guide.md # Style Dictionary configuration
│   └── platform-exports.md      # iOS, Android, React Native
│
├── tokens/                      # Source tokens (Style Dictionary format)
│   ├── global/
│   │   ├── colors.json          # Universal color palette
│   │   ├── spacing.json         # Spacing scale (logical properties)
│   │   ├── typography.json      # Base typography
│   │   ├── borders.json         # Border widths and radii
│   │   ├── shadows.json         # Elevation shadows
│   │   ├── motion.json          # Animation durations/easing
│   │   └── z-index.json         # Layering system
│   ├── themes/
│   │   ├── light.json           # Light theme overrides
│   │   ├── dark.json            # Dark theme overrides
│   │   └── high-contrast.json   # High contrast theme
│   └── languages/
│       ├── ar.json              # Arabic: fonts, line-height, spacing
│       ├── he.json              # Hebrew: fonts, text direction
│       ├── ja.json              # Japanese: fonts, spacing
│       ├── ko.json              # Korean: fonts
│       ├── zh-CN.json           # Chinese Simplified: fonts
│       └── de.json              # German: spacing adjustments
│
├── build/                       # Generated output (from Style Dictionary)
│   ├── css/
│   │   ├── variables.css        # Base CSS custom properties
│   │   ├── variables-light.css  # Light theme
│   │   ├── variables-dark.css   # Dark theme
│   │   ├── variables-ar.css     # Arabic overrides
│   │   └── variables-ja.css     # Japanese overrides
│   ├── scss/
│   │   └── _variables.scss      # SCSS variables
│   ├── js/
│   │   └── tokens.js            # JavaScript/TypeScript tokens
│   ├── ios/
│   │   └── Tokens.swift         # iOS Swift tokens
│   └── android/
│       ├── colors.xml           # Android color resources
│       └── dimens.xml           # Android dimension resources
│
├── config.js                    # Style Dictionary configuration
│
├── scripts/
│   ├── build-tokens.sh          # Build all tokens with Style Dictionary
│   ├── generate_theme.py        # Generate theme from config
│   ├── generate_color_scale.py  # Create 9-shade palette
│   ├── validate_tokens.py       # Ensure consistency
│   ├── validate_contrast.py     # Check WCAG compliance
│   ├── validate_rtl.py          # Test RTL compatibility
│   └── export_platform.py       # Export to iOS, Android
│
├── examples/
│   ├── theme-switcher.tsx      # Theme toggle component
│   ├── token-usage.tsx         # How to use tokens
│   ├── custom-theme.tsx        # Creating custom theme
│   └── brand-customization.md  # Guide to brand theming
│
└── assets/
    └── color-scales/           # Visual reference of color palettes
```

---

### SKILL.md Frontmatter

```yaml
---
name: design-tokens-theming
description: Comprehensive design token system and theming framework for consistent, customizable UI styling across all components. Use when implementing visual design, creating brand themes, switching between light/dark modes, or ensuring design consistency. Covers complete token taxonomy (color, typography, spacing, shadows, borders, motion, z-index), theme switching mechanisms (CSS custom properties, theme providers), accessibility considerations (WCAG contrast, high contrast themes, reduced motion), and platform-specific exports (web, iOS, Android). Provides light/dark themes, brand customization examples, and token generation tools. This is the foundational styling layer referenced by ALL component skills. Triggered by requests to: theme components, implement light/dark mode, create brand styles, customize visual design, ensure design consistency, or apply styling to components.
---
```

---

## Integration with Component Skills

### How Component Skills Reference This

Each component skill should include a **"Styling & Theming"** section:

```markdown
## Styling & Theming

This component uses design tokens from the **design-tokens** skill for all visual styling.

### Default Token Usage

See `design-tokens/references/component-tokens.md` for complete reference.

**Button Tokens:**
- `--button-bg-primary` - Primary button background
- `--button-text-primary` - Primary button text color
- `--button-padding-x` - Horizontal padding
- `--button-padding-y` - Vertical padding
- `--button-border-radius` - Corner radius
- `--button-font-size` - Text size
- `--button-font-weight` - Text weight

### Custom Theming

Override these tokens in your theme file to customize button appearance.

**Example:**
\```css
:root[data-theme="custom"] {
  --button-bg-primary: #FF6B35;
  --button-border-radius: 20px;
}
\```
```

---

## Migration Strategy

### For Existing Component Skills

**Add to each init.md:**

```markdown
## Styling & Theming

This component uses the **design-tokens** skill for visual styling.

### Token Categories Used
- Colors: [list specific tokens]
- Spacing: [list specific tokens]
- Typography: [list specific tokens]
- Borders: [list specific tokens]

### Theme Support
- ✅ Light mode
- ✅ Dark mode
- ✅ High contrast
- ✅ Custom brand themes

See `design-tokens/` skill for complete theming documentation.
```

---

## Key Takeaways

1. **Design tokens are the foundation** - All visual styling flows from tokens
2. **3-level hierarchy** - Primitive → Semantic → Component tokens
3. **7 core categories** - Color, spacing, typography, borders, shadows, motion, z-index
4. **Theme switching built-in** - Light, dark, high contrast, custom brands
5. **Accessibility first** - WCAG compliance, reduced motion, high contrast
6. **Platform agnostic** - Export to web, iOS, Android, React Native
7. **Separation of concerns** - Component behavior separate from visual styling
8. **Referenced by all skills** - Every component skill uses design tokens

**This is a game-changing architectural decision that makes the component library infinitely adaptable.**

---

**END OF MASTER PLAN**

*The design tokens skill is the foundational styling layer for the entire component library. All component skills reference this for visual styling, enabling brand customization, theme switching, and design consistency.*
