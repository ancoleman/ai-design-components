# Style Dictionary Setup Guide

**Transform W3C design tokens to multiple platform formats**

---

## What is Style Dictionary?

Style Dictionary transforms design tokens from JSON to platform-specific formats:

```
JSON Tokens → Style Dictionary → CSS Variables
                               → SCSS Variables
                               → iOS Swift
                               → Android XML
                               → JavaScript
```

**Industry standard** - Used by Amazon, Adobe, Salesforce, IBM

---

## Installation

```bash
npm install --save-dev style-dictionary
```

---

## Configuration

**File:** `config.js`

```javascript
import StyleDictionary from 'style-dictionary';

export default {
  // Source token files
  source: [
    'tokens/global/**/*.json',
    'tokens/themes/light.json',
    'tokens/components/**/*.json'
  ],

  // Platform outputs
  platforms: {
    // CSS Custom Properties
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables',
        options: {
          outputReferences: true,  // Use var() for references
          showFileHeader: true
        }
      }]
    },

    // Dark theme (separate file)
    'css-dark': {
      transformGroup: 'css',
      buildPath: 'build/css/',
      source: [
        'tokens/global/**/*.json',
        'tokens/themes/dark.json',
        'tokens/components/**/*.json'
      ],
      files: [{
        destination: 'variables-dark.css',
        format: 'css/variables',
        options: {
          outputReferences: true,
          selector: ':root[data-theme="dark"]'
        }
      }]
    },

    // SCSS Variables
    scss: {
      transformGroup: 'scss',
      buildPath: 'build/scss/',
      files: [{
        destination: '_variables.scss',
        format: 'scss/variables'
      }]
    },

    // JavaScript/TypeScript
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

---

## Building Tokens

```bash
# Build all platforms
npm run build
# or
style-dictionary build --config config.js

# Watch mode (auto-rebuild on changes)
npm run build:watch
# or
style-dictionary build --config config.js --watch
```

---

## Output Examples

### Input (W3C JSON)

```json
{
  "color": {
    "primary": {
      "$value": "#3B82F6",
      "$type": "color"
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

### Output: CSS Variables

```css
/* build/css/variables.css */
:root {
  --color-primary: #3B82F6;
  --spacing-md: 16px;
}
```

### Output: SCSS

```scss
/* build/scss/_variables.scss */
$color-primary: #3B82F6;
$spacing-md: 16px;
```

### Output: JavaScript

```javascript
// build/js/tokens.js
export const color = {
  primary: '#3B82F6'
};

export const spacing = {
  md: '16px'
};
```

### Output: iOS Swift

```swift
// build/ios/DesignTokens.swift
public class DesignTokens {
  public static let colorPrimary = UIColor(hex: "#3B82F6")
  public static let spacingMd = CGFloat(16)
}
```

### Output: Android XML

```xml
<!-- build/android/res/values/colors.xml -->
<resources>
  <color name="color_primary">#3B82F6</color>
</resources>

<!-- build/android/res/values/dimens.xml -->
<resources>
  <dimen name="spacing_md">16dp</dimen>
</resources>
```

---

## Token References

**W3C format supports references:**

```json
{
  "color": {
    "blue": {
      "500": {
        "$value": "#3B82F6",
        "$type": "color"
      }
    },
    "primary": {
      "$value": "{color.blue.500}",
      "$type": "color"
    }
  }
}
```

**CSS output with `outputReferences: true`:**

```css
:root {
  --color-blue-500: #3B82F6;
  --color-primary: var(--color-blue-500);  /* ✅ Reference preserved */
}
```

**Why this matters:**
- Changing `--color-blue-500` updates `--color-primary` automatically
- Enables dynamic theming

---

## Multi-Theme Build

**Build separate CSS files for each theme:**

```javascript
// config.js
export default {
  platforms: {
    'css-light': {
      transformGroup: 'css',
      buildPath: 'build/css/',
      source: ['tokens/global/**/*.json', 'tokens/themes/light.json'],
      files: [{
        destination: 'variables-light.css',
        format: 'css/variables',
        options: { selector: ':root' }
      }]
    },
    'css-dark': {
      transformGroup: 'css',
      buildPath: 'build/css/',
      source: ['tokens/global/**/*.json', 'tokens/themes/dark.json'],
      files: [{
        destination: 'variables-dark.css',
        format: 'css/variables',
        options: { selector: ':root[data-theme="dark"]' }
      }]
    }
  }
};
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "build": "style-dictionary build --config config.js",
    "build:watch": "style-dictionary build --config config.js --watch",
    "clean": "rm -rf build/",
    "validate": "python scripts/validate_tokens.py",
    "validate:contrast": "python scripts/validate_contrast.py"
  },
  "devDependencies": {
    "style-dictionary": "^4.0.0"
  }
}
```

---

## Usage in Projects

### CSS

```html
<!-- Load generated CSS -->
<link rel="stylesheet" href="build/css/variables.css">
<link rel="stylesheet" href="build/css/variables-dark.css">
```

```css
/* Use in your styles */
.button {
  background-color: var(--button-bg-primary);
  padding: var(--spacing-md);
}
```

### SCSS

```scss
// Import generated variables
@import 'build/scss/variables';

.button {
  background-color: $button-bg-primary;
  padding: $spacing-md;
}
```

### JavaScript/TypeScript

```typescript
import { color, spacing } from './build/js/tokens';

const buttonStyles = {
  backgroundColor: color.primary,
  padding: spacing.md
};
```

---

## Resources

- **Style Dictionary Docs:** https://styledictionary.com
- **GitHub:** https://github.com/amzn/style-dictionary
- **Context7:** `/amzn/style-dictionary`

---

**Configuration file:** `config.js` in skill root
