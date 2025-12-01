# Design Tokens & Theming System

**Foundational styling layer for the ai-design-components skill library**

Version: 1.0.0 | Status: ✅ Complete | W3C Compliant

---

## Overview

The design-tokens skill provides the **foundational styling architecture** for all component skills in the ai-design-components library. It enables:

- 🎨 **Theme Switching**: Light/dark mode, high-contrast, custom brand themes
- 🌍 **RTL/i18n Support**: CSS logical properties for automatic right-to-left language support
- ♿ **Accessibility**: WCAG 2.1 AA compliant color combinations, high-contrast themes, reduced motion
- 🚀 **Multi-Platform**: Export to CSS, SCSS, iOS Swift, Android XML, JavaScript/TypeScript
- 🔗 **Skill Chaining**: Component skills reference tokens for consistent, themeable styling

---

## Quick Start

### 1. Build Tokens

```bash
# Install dependencies
npm install

# Build tokens for all platforms
npm run build

# Watch mode (auto-rebuild on changes)
npm run build:watch
```

**Generates:**
- `build/css/variables.css` - CSS custom properties (light theme)
- `build/css/variables-dark.css` - Dark theme overrides
- `build/css/variables-high-contrast.css` - High-contrast theme
- `build/scss/_variables.scss` - SCSS variables
- `build/js/tokens.js` - JavaScript/TypeScript tokens
- `build/ios/DesignTokens.swift` - iOS Swift tokens

---

### 2. Use in Your Project

**HTML:**
```html
<link rel="stylesheet" href="build/css/variables.css">
<link rel="stylesheet" href="build/css/variables-dark.css">
```

**CSS:**
```css
.button {
  background-color: var(--button-bg-primary);
  color: var(--button-text-primary);
  padding-inline: var(--button-padding-inline);
  border-radius: var(--button-border-radius);
}
```

**JavaScript (theme switching):**
```javascript
document.documentElement.setAttribute('data-theme', 'dark');
```

---

## Token Taxonomy

**7 Core Categories:**

1. **Color** (`tokens/global/colors.json`)
   - 9-shade palettes: gray, blue, purple, green, yellow, red, orange
   - Semantic colors: primary, success, warning, error, text, backgrounds, borders

2. **Spacing** (`tokens/global/spacing.json`)
   - 4px base scale (0, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 32)
   - Semantic spacing: xs, sm, md, lg, xl, 2xl, 3xl

3. **Typography** (`tokens/global/typography.json`)
   - Font families: sans, serif, mono
   - Type scale: xs → 7xl (12px → 72px)
   - Font weights: thin → black (100 → 900)
   - Line heights: tight, normal, relaxed

4. **Borders** (`tokens/global/borders.json`)
   - Border widths: thin, medium, thick
   - Border radius: sm → full (4px → 9999px)

5. **Shadows** (`tokens/global/shadows.json`)
   - Elevation: xs → 2xl
   - Focus rings (colored)
   - Inner shadows

6. **Motion** (`tokens/global/motion.json`)
   - Durations: instant → slower (100ms → 700ms)
   - Easing: linear, in, out, in-out, bounce

7. **Z-Index** (`tokens/global/z-index.json`)
   - Layering: base → notification (0 → 1080)

---

## Token Hierarchy

**3-Tier Architecture:**

```
Primitive Tokens (Foundation)
    ↓ referenced by
Semantic Tokens (Purpose)
    ↓ referenced by
Component Tokens (Specific)
    ↓ used by
Component Skills (forms, data-viz, tables, etc.)
```

**Example:**
```
--color-blue-500 (Primitive)
    ↓
--color-primary (Semantic)
    ↓
--button-bg-primary (Component)
    ↓
<button> in forms skill
```

---

## Themes

**3 Built-in Themes:**

1. **Light** (`tokens/themes/light.json`) - Default theme
2. **Dark** (`tokens/themes/dark.json`) - Dark mode overrides
3. **High-Contrast** (`tokens/themes/high-contrast.json`) - WCAG AAA (7:1 contrast)

**Custom Themes:**
Create your own by overriding token values:

```css
:root[data-theme="my-brand"] {
  --color-primary: #FF6B35;
  --font-sans: 'Poppins', sans-serif;
  --radius-md: 12px;
}
```

---

## CSS Logical Properties (RTL Support)

**All tokens use logical properties for automatic RTL support:**

```css
/* ✅ CORRECT - Auto-flips in RTL */
--button-padding-inline: 24px;
--icon-margin-inline-end: 4px;

/* ❌ WRONG - Won't flip in RTL */
--button-padding-left: 24px;
--icon-margin-right: 4px;
```

**Supported languages:** Arabic, Hebrew, Persian, Urdu (RTL), plus all LTR languages

---

## Component Integration

**All component skills reference design tokens:**

**Button (from forms skill):**
```css
.button {
  background-color: var(--button-bg-primary);
  padding-inline: var(--button-padding-inline);
  border-radius: var(--button-border-radius);
}
```

**Chart (from data-viz skill):**
```tsx
<Line stroke="var(--chart-color-1)" />
```

**Complete integration guide:** `SKILL_CHAINING_ARCHITECTURE.md`

---

## File Structure

```
design-tokens/
├── SKILL.md                              # Main skill file (878 lines)
├── SKILL_CHAINING_ARCHITECTURE.md        # Integration guide for component skills
├── init.md                               # Master plan (1845 lines)
├── README.md                             # This file
├── config.js                             # Style Dictionary configuration
├── package.json                          # Dependencies
│
├── tokens/                               # W3C format source tokens
│   ├── global/
│   │   ├── colors.json                   # Color primitives (9-shade palettes)
│   │   ├── spacing.json                  # Spacing scale (4px base)
│   │   ├── typography.json               # Fonts, sizes, weights, line heights
│   │   ├── borders.json                  # Border widths and radii
│   │   ├── shadows.json                  # Elevation shadows
│   │   ├── motion.json                   # Animation durations and easing
│   │   └── z-index.json                  # Layering system
│   ├── themes/
│   │   ├── light.json                    # Light theme (semantic mappings)
│   │   ├── dark.json                     # Dark theme overrides
│   │   └── high-contrast.json            # High-contrast theme (WCAG AAA)
│   ├── components/
│   │   ├── button.json                   # Button component tokens
│   │   ├── input.json                    # Input component tokens
│   │   └── chart.json                    # Chart component tokens (data-viz)
│   └── languages/
│       ├── ar.json                       # Arabic overrides
│       └── ja.json                       # Japanese overrides
│
├── build/                                # Generated output (from Style Dictionary)
│   ├── css/
│   │   ├── variables.css                 # Light theme CSS variables
│   │   ├── variables-dark.css            # Dark theme CSS variables
│   │   └── variables-high-contrast.css   # High-contrast CSS variables
│   ├── scss/
│   │   └── _variables.scss               # SCSS variables
│   ├── js/
│   │   ├── tokens.js                     # JavaScript ES6 tokens
│   │   └── tokens.d.ts                   # TypeScript declarations
│   └── ios/
│       └── DesignTokens.swift            # iOS Swift tokens
│
├── scripts/                              # Token-free execution scripts
│   ├── generate_color_scale.py          # Generate 9-shade palette
│   ├── validate_tokens.py                # Validate W3C format
│   ├── validate_contrast.py              # Check WCAG compliance
│   └── validate_logical_properties.py    # Verify RTL support
│
├── references/                           # Progressive disclosure docs
│   ├── component-integration.md          # How components use tokens
│   ├── theme-switching.md                # Theme implementation guide
│   ├── logical-properties.md             # CSS logical properties reference
│   ├── accessibility-tokens.md           # WCAG compliance guide
│   └── style-dictionary-setup.md         # Build system documentation
│
└── examples/                             # Working code examples
    ├── ThemeProvider.tsx                 # React theme context
    ├── ThemeToggle.tsx                   # Theme toggle component
    ├── TokenUsageExample.tsx             # Token usage patterns
    └── theme-switcher.html               # Vanilla JS demo
```

---

## Usage Examples

### React with Theme Provider

```tsx
// App.tsx
import { ThemeProvider } from './design-tokens/examples/ThemeProvider';
import { ThemeToggle } from './design-tokens/examples/ThemeToggle';

function App() {
  return (
    <ThemeProvider>
      <ThemeToggle />
      <YourComponents />
    </ThemeProvider>
  );
}
```

### Vanilla JavaScript

```javascript
// Set theme
function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('theme', themeName);
}

// Toggle light/dark
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
}
```

### Component with Tokens

```css
.my-component {
  /* Use component tokens */
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);

  /* Use logical properties for RTL */
  padding-inline: var(--spacing-md);
  padding-block: var(--spacing-sm);

  /* Reference other categories */
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-fast);
}
```

---

## Scripts & Validation

### Generate Color Scale

```bash
# Create 9-shade palette from base color
python scripts/generate_color_scale.py \
  --base "#FF6B35" \
  --name "brand-orange" \
  --output tokens/global/colors-custom.json
```

### Validate Tokens

```bash
# Validate W3C format and naming
npm run validate

# Check WCAG color contrast
npm run validate:contrast

# Verify RTL compatibility
npm run validate:rtl
```

---

## W3C Compliance

**Specification:** [Design Tokens Community Group 2025.10](https://www.designtokens.org/tr/2025.10/)

**Required properties:**
- `$value` - Token value
- `$type` - Token type (color, dimension, fontSize, etc.)

**Optional properties:**
- `$description` - Human-readable description
- `$extensions` - Custom metadata

**Token references:**
```json
{
  "color": {
    "primary": {
      "$value": "{color.blue.500}",
      "$type": "color"
    }
  }
}
```

---

## Accessibility Features

✅ **WCAG 2.1 AA Compliant**
- All text/background combinations meet 4.5:1 contrast
- UI components meet 3:1 contrast
- Validated with `scripts/validate_contrast.py`

✅ **High-Contrast Theme**
- 7:1 contrast ratio (WCAG AAA)
- Auto-applies via `prefers-contrast: high` media query

✅ **Reduced Motion**
- Honors `prefers-reduced-motion: reduce`
- Disables all animations when requested

✅ **Colorblind-Safe**
- Chart colors use IBM/Paul Tol palettes
- No red/green reliance

---

## Component Token Naming

**Convention:**
```
--{component}-{property}-{variant?}-{state?}
```

**Examples:**
- `--button-bg-primary`
- `--button-bg-primary-hover`
- `--input-border-color-focus`
- `--chart-color-1`

**Complete naming guide:** `SKILL_CHAINING_ARCHITECTURE.md`

---

## Integration with Other Skills

**This skill is referenced by:**
- ✅ `data-viz` - Chart color palettes, axis colors, tooltips
- ✅ `forms` - Button, input, select, checkbox styling
- 🚧 `tables` - Table borders, row colors, headers
- 🚧 `dashboards` - Layout spacing, card styling
- 🚧 All other component skills

**How to integrate:**
See `SKILL_CHAINING_ARCHITECTURE.md` for complete integration architecture.

---

## Testing

### Visual Testing

```bash
# Open theme switcher demo
open examples/theme-switcher.html
```

**Test checklist:**
- [ ] Light theme displays correctly
- [ ] Dark theme displays correctly
- [ ] High-contrast theme displays correctly
- [ ] Theme persists after reload
- [ ] No FOUC (flash of unstyled content)
- [ ] RTL mode works (`<html dir="rtl">`)

### Automated Testing

```bash
# Validate token structure
npm run validate

# Check color contrast (WCAG)
npm run validate:contrast

# Verify RTL compatibility
npm run validate:rtl
```

---

## Key Files

**Documentation:**
- `SKILL.md` - Main skill file (progressive disclosure)
- `SKILL_CHAINING_ARCHITECTURE.md` - Component integration guide
- `init.md` - Complete master plan
- `references/` - Detailed documentation

**Source Tokens (W3C format):**
- `tokens/global/` - Primitive tokens (colors, spacing, etc.)
- `tokens/themes/` - Theme overrides (light, dark, high-contrast)
- `tokens/components/` - Component-specific tokens
- `tokens/languages/` - Language-specific overrides

**Build System:**
- `config.js` - Style Dictionary configuration
- `package.json` - Build scripts
- `build/` - Generated output

**Scripts:**
- `scripts/generate_color_scale.py` - Generate color palettes
- `scripts/validate_tokens.py` - W3C format validation
- `scripts/validate_contrast.py` - WCAG compliance checker
- `scripts/validate_logical_properties.py` - RTL verification

**Examples:**
- `examples/ThemeProvider.tsx` - React theme context
- `examples/ThemeToggle.tsx` - Theme switcher component
- `examples/TokenUsageExample.tsx` - Usage patterns
- `examples/theme-switcher.html` - Vanilla JS demo

---

## Architecture Principles

### Separation of Concerns

```
Component Skills = Behavior + Structure (NO visual styling)
Design Tokens = Visual Styling Variables
Themes = Token Value Overrides
```

**Result:** Components are infinitely customizable without code changes

### Progressive Disclosure

```
SKILL.md (878 lines) → Quick start, overview, references
    ↓
references/ → Detailed documentation
    ↓
scripts/ → Executable utilities (token-free)
```

### Token-Free Scripts

Scripts execute **without loading into context** (zero token cost):

```bash
python scripts/generate_color_scale.py   # 0 tokens
python scripts/validate_contrast.py      # 0 tokens
```

---

## Resources

**Specifications:**
- [W3C Design Tokens Spec 2025.10](https://www.designtokens.org/tr/2025.10/)
- [CSS Logical Properties (W3C)](https://www.w3.org/TR/css-logical-1/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

**Tools:**
- [Style Dictionary](https://styledictionary.com) - Token transformation
- [Tokens Studio](https://tokens.studio) - Figma plugin (optional)

**Testing:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Sim Daltonism](https://michelf.ca/projects/sim-daltonism/) - Colorblind simulator

---

## License

MIT - Part of ai-design-components

---

## Contributing

See parent repository for contribution guidelines.

**Skill development follows:** `../skill_best_practice.md` (Anthropic's official Skills guide)

---

## Changelog

**v1.0.0** (November 13, 2025)
- ✅ Complete W3C-compliant token system
- ✅ 7 token categories (color, spacing, typography, borders, shadows, motion, z-index)
- ✅ 3 built-in themes (light, dark, high-contrast)
- ✅ CSS logical properties for RTL support
- ✅ Multi-platform exports (CSS, SCSS, iOS, Android, JS)
- ✅ WCAG 2.1 AA compliant
- ✅ Skill chaining architecture
- ✅ Token generation and validation scripts
- ✅ Complete documentation and examples

---

**Built following Anthropic's Skills best practices**

Progressive disclosure | Token-efficient | W3C compliant | Production-ready
