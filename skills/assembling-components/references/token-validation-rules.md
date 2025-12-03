# Token Validation Rules

> Complete reference for CSS design token validation rules used by `validate_tokens.py`.

## Overview

The token validation script scans CSS files for hardcoded values that should use design tokens. This ensures consistent theming and makes dark mode, brand customization, and accessibility features work correctly.

## Severity Levels

| Level | Meaning | CI/CD Impact |
|-------|---------|--------------|
| **Error** | Must fix before deployment | Build fails |
| **Warning** | Should fix but not blocking | Build succeeds |
| **Info** | Nice to have (strict mode only) | No impact |

## Validation Rules

### 1. Colors (Error)

**Pattern:** Hardcoded hex, rgb, rgba, hsl values

**Bad:**
```css
.button {
  background: #FA582D;
  color: rgb(30, 41, 59);
  border-color: rgba(0, 0, 0, 0.1);
}
```

**Good:**
```css
.button {
  background: var(--color-primary);
  color: var(--color-text-primary);
  border-color: var(--color-border-primary);
}
```

**Common Token Mappings:**

| Hardcoded | Token |
|-----------|-------|
| `#FA582D` | `--color-cyber-orange` / `--color-primary` |
| `#00C0E8` | `--color-prisma-blue` / `--color-info` |
| `#00CC66` | `--color-cortex-green` / `--color-success` |
| `#FFCB06` | `--color-strata-yellow` / `--color-warning` |
| `#C84727` | `--color-unit42-red` / `--color-error` |
| `#FFFFFF` | `--color-bg-primary` |
| `#F8FAFC` | `--color-bg-secondary` |
| `#1E293B` | `--color-text-primary` |
| `#64748B` | `--color-text-secondary` |

**Exceptions:**
- `currentColor` - CSS keyword
- `transparent` - CSS keyword
- `inherit` - CSS keyword

### 2. Spacing (Error)

**Pattern:** Hardcoded pixel values ≥ 4px on spacing properties

**Properties:** `padding`, `margin`, `gap`, `top`, `right`, `bottom`, `left`

**Bad:**
```css
.card {
  padding: 16px;
  margin-bottom: 24px;
  gap: 8px;
}
```

**Good:**
```css
.card {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  gap: var(--spacing-sm);
}
```

**Token Scale:**

| Hardcoded | Token | Base Unit |
|-----------|-------|-----------|
| `4px` | `--spacing-xs` / `--space-1` | 1× |
| `8px` | `--spacing-sm` / `--space-2` | 2× |
| `12px` | `--space-3` | 3× |
| `16px` | `--spacing-md` / `--space-4` | 4× |
| `20px` | `--space-5` | 5× |
| `24px` | `--spacing-lg` / `--space-6` | 6× |
| `32px` | `--spacing-xl` / `--space-8` | 8× |
| `40px` | `--space-10` | 10× |
| `48px` | `--spacing-2xl` / `--space-12` | 12× |

**Exceptions:**
- `0`, `0px` - Zero values
- `1px` - Hairline borders
- `2px` - Focus outlines

### 3. Font Sizes (Error)

**Pattern:** Hardcoded font-size values

**Bad:**
```css
.title {
  font-size: 24px;
}
.body {
  font-size: 14px;
}
```

**Good:**
```css
.title {
  font-size: var(--font-size-2xl);
}
.body {
  font-size: var(--font-size-sm);
}
```

**Token Scale:**

| Hardcoded | Token | rem |
|-----------|-------|-----|
| `12px` | `--font-size-xs` | 0.75rem |
| `14px` | `--font-size-sm` | 0.875rem |
| `16px` | `--font-size-base` | 1rem |
| `18px` | `--font-size-lg` | 1.125rem |
| `20px` | `--font-size-xl` | 1.25rem |
| `24px` | `--font-size-2xl` | 1.5rem |
| `30px` | `--font-size-3xl` | 1.875rem |
| `36px` | `--font-size-4xl` | 2.25rem |

### 4. Border Radius (Warning)

**Pattern:** Hardcoded border-radius values

**Bad:**
```css
.button {
  border-radius: 8px;
}
.avatar {
  border-radius: 9999px;
}
```

**Good:**
```css
.button {
  border-radius: var(--radius-md);
}
.avatar {
  border-radius: var(--radius-full);
}
```

**Token Scale:**

| Hardcoded | Token |
|-----------|-------|
| `4px` | `--radius-sm` |
| `8px` | `--radius-md` |
| `12px` | `--radius-lg` |
| `16px` | `--radius-xl` |
| `9999px` | `--radius-full` |

### 5. Box Shadows (Warning)

**Pattern:** Hardcoded box-shadow values

**Bad:**
```css
.card {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.modal {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

**Good:**
```css
.card {
  box-shadow: var(--shadow-sm);
}
.modal {
  box-shadow: var(--shadow-2xl);
}
```

**Token Scale:**

| Token | Description |
|-------|-------------|
| `--shadow-sm` | Subtle elevation |
| `--shadow-md` | Cards, dropdowns |
| `--shadow-lg` | Popovers |
| `--shadow-xl` | Modals, dialogs |
| `--shadow-2xl` | Overlays |

### 6. Transitions (Info - Strict Mode Only)

**Pattern:** Hardcoded transition timing

**Bad:**
```css
.button {
  transition: all 150ms ease;
}
```

**Good:**
```css
.button {
  transition: var(--transition-fast);
}
```

**Token Scale:**

| Token | Duration |
|-------|----------|
| `--duration-fast` | 150ms |
| `--duration-normal` | 200ms |
| `--duration-slow` | 300ms |
| `--transition-fast` | all 150ms ease-out |
| `--transition-normal` | all 200ms ease-out |

### 7. Z-Index (Warning)

**Pattern:** Hardcoded z-index values ≥ 100

**Bad:**
```css
.dropdown {
  z-index: 1000;
}
.modal {
  z-index: 1050;
}
```

**Good:**
```css
.dropdown {
  z-index: var(--z-dropdown);
}
.modal {
  z-index: var(--z-modal);
}
```

**Token Scale:**

| Token | Value |
|-------|-------|
| `--z-dropdown` | 1000 |
| `--z-sticky` | 1020 |
| `--z-fixed` | 1030 |
| `--z-modal-backdrop` | 1040 |
| `--z-modal` | 1050 |
| `--z-popover` | 1060 |
| `--z-tooltip` | 1070 |
| `--z-toast` | 1080 |

## Exceptions (Always Allowed)

### CSS Keywords
- `currentColor`
- `transparent`
- `inherit`
- `initial`
- `unset`
- `none`
- `auto`

### Small Values
- `0`, `0px` - Zero
- `1px` - Hairline borders
- `2px` - Focus outlines
- `100%`, `50%` - Percentages

### Layout Values
These are skipped because they're structural, not themeable:
- Container max-widths (`1400px`, `1200px`, `1024px`)
- Media query breakpoints (`768px`, `640px`, `480px`)
- Grid functions (`minmax()`, `repeat()`)
- Grid templates

### Context-Specific
- Lines starting with `--` (token definitions)
- Comments (`/*`, `*`, `*/`)
- `@media` query lines
- `@keyframes` definitions
- Animation percentages (`0%`, `100%`)

### Exception Properties
Some properties accept hardcoded values:
- `outline` - Accessibility focus indicators
- `outline-offset` - Accessibility
- `transform` - Animation transforms
- `animation` - Animation definitions
- `content` - Pseudo-element content
- `clip-path` - Complex clipping
- `mask` - Complex masking

## Script Usage

```bash
# Basic validation
python scripts/validate_tokens.py src/styles

# Strict mode (includes info-level)
python scripts/validate_tokens.py src --strict

# JSON output for CI/CD
python scripts/validate_tokens.py src --json

# Show fix suggestions
python scripts/validate_tokens.py src --fix-suggestions
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Validate CSS Tokens
  run: python scripts/validate_tokens.py src --json > token-report.json

- name: Check for Errors
  run: |
    errors=$(jq '.errors' token-report.json)
    if [ "$errors" -gt 0 ]; then
      echo "Found $errors token violations"
      exit 1
    fi
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python scripts/validate_tokens.py src --strict
if [ $? -ne 0 ]; then
  echo "CSS token validation failed. Fix violations before committing."
  exit 1
fi
```

## Output Example

```
======================================================================
  CSS DESIGN TOKEN VALIDATION REPORT
======================================================================

  src/components/Card.css
  ------------------------------------------------------------
    ❌ Line 5:12 [ERROR]
       Found: #FA582D
       Rule: colors
       Fix: Use semantic color token (e.g., --color-primary)
       Suggested: var(--color-cyber-orange)

    ⚠️ Line 12:3 [WARNING]
       Found: border-radius: 8px
       Rule: radii
       Fix: Use radius token (e.g., --radius-md)
       Suggested: var(--radius-md)

----------------------------------------------------------------------
  SUMMARY
----------------------------------------------------------------------
  Files scanned:     15
  Files with issues: 3
  Total violations:  7
    - Errors:   4
    - Warnings: 3
    - Info:     0

  By Category:
    - colors: 4
    - radii: 2
    - shadows: 1
```
