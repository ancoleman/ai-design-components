# Accessibility Token Reference

**WCAG 2.1 compliant design tokens for accessible interfaces**


## Table of Contents

- [WCAG Contrast Requirements](#wcag-contrast-requirements)
- [Color Contrast Validation](#color-contrast-validation)
  - [Pre-Validated Color Pairs](#pre-validated-color-pairs)
  - [Validation Script](#validation-script)
- [High-Contrast Theme](#high-contrast-theme)
- [Reduced Motion](#reduced-motion)
- [Focus Indicators](#focus-indicators)
- [Color Blindness Considerations](#color-blindness-considerations)
  - [Colorblind-Safe Palettes](#colorblind-safe-palettes)
  - [Don't Rely on Color Alone](#dont-rely-on-color-alone)
- [Accessibility Checklist](#accessibility-checklist)
  - [Token Design](#token-design)
  - [Implementation](#implementation)
  - [Testing Tools](#testing-tools)
- [Resources](#resources)

---

## WCAG Contrast Requirements

**WCAG 2.1 Level AA:**
- Normal text (< 18px): **4.5:1** minimum
- Large text (≥ 18px or 14px bold): **3:1** minimum
- UI components: **3:1** minimum

**WCAG 2.1 Level AAA:**
- Normal text: **7:1** minimum
- Large text: **4.5:1** minimum

---

## Color Contrast Validation

### Pre-Validated Color Pairs

**Light Theme (AA Compliant):**
```css
/* Text on backgrounds */
--color-text-primary: #111827;    /* gray-900 */
--color-bg-primary: #FFFFFF;
/* Ratio: 17.7:1 ✅ (AAA) */

--color-text-secondary: #4B5563;  /* gray-600 */
--color-bg-primary: #FFFFFF;
/* Ratio: 7.1:1 ✅ (AAA) */

--color-text-tertiary: #9CA3AF;   /* gray-400 */
--color-bg-primary: #FFFFFF;
/* Ratio: 3.2:1 ✅ (AA large text only) */
```

**Dark Theme (AA Compliant):**
```css
--color-text-primary: #F9FAFB;    /* gray-50 */
--color-bg-primary: #111827;      /* gray-900 */
/* Ratio: 17.7:1 ✅ (AAA) */

--color-text-secondary: #D1D5DB;  /* gray-300 */
--color-bg-primary: #111827;
/* Ratio: 9.8:1 ✅ (AAA) */
```

### Validation Script

```bash
# Check all color combinations
python scripts/validate_contrast.py
```

---

## High-Contrast Theme

**For users with visual impairments:**

```css
:root[data-theme="high-contrast"] {
  /* Pure colors */
  --color-primary: #0000FF;        /* Pure blue */
  --color-text-primary: #000000;   /* Pure black */
  --color-background: #FFFFFF;     /* Pure white */
  --color-border: #000000;         /* Black borders */

  /* 7:1 minimum contrast (AAA) */
  --color-text-secondary: #333333;

  /* Stronger shadows */
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.5);

  /* Thicker borders */
  --border-width-thin: 2px;
}
```

**Auto-apply via system preference:**
```css
@media (prefers-contrast: high) {
  :root {
    /* Apply high-contrast token values */
  }
}
```

---

## Reduced Motion

**Honor user's motion preference:**

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    /* Disable all animations */
    --duration-instant: 0ms;
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;

    /* Remove transitions */
    --transition-fast: none;
    --transition-normal: none;
    --transition-slow: none;

    /* Disable animations */
    --ease-in: linear;
    --ease-out: linear;
  }
}
```

**JavaScript detection:**
```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  console.log('Reduced motion enabled');
}
```

---

## Focus Indicators

**Visible focus states for keyboard navigation:**

```css
:root {
  /* Focus ring tokens */
  --shadow-focus-primary: 0 0 0 3px rgba(59, 130, 246, 0.3);
  --shadow-focus-error: 0 0 0 3px rgba(239, 68, 68, 0.3);
  --shadow-focus-success: 0 0 0 3px rgba(34, 197, 94, 0.3);

  /* High-contrast focus (thicker, darker) */
  --shadow-focus-high-contrast: 0 0 0 4px rgba(0, 0, 255, 0.6);
}

/* Apply to interactive elements */
.button:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus-primary);
}

.input:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus-primary);
}

/* High-contrast override */
:root[data-theme="high-contrast"] .button:focus-visible {
  box-shadow: var(--shadow-focus-high-contrast);
}
```

**Never remove focus indicators:**
```css
/* ❌ WRONG - Removes keyboard navigation indicator */
button:focus {
  outline: none;
}

/* ✅ CORRECT - Custom focus indicator */
button:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus-primary);
}
```

---

## Color Blindness Considerations

### Colorblind-Safe Palettes

**Built into chart tokens** (`tokens/components/chart.json`):

```css
/* IBM Colorblind-Safe Palette */
--chart-color-1: #648FFF;  /* Blue */
--chart-color-2: #785EF0;  /* Purple */
--chart-color-3: #DC267F;  /* Magenta */
--chart-color-4: #FE6100;  /* Orange */
--chart-color-5: #FFB000;  /* Yellow */
```

**Avoid red/green combinations:**
- 8% of males have red-green colorblindness
- Use blue/orange, purple/yellow instead

### Don't Rely on Color Alone

```css
/* ❌ Color only */
.status-success {
  color: var(--color-success);
}

/* ✅ Color + icon/pattern */
.status-success::before {
  content: '✓ ';
  color: var(--color-success);
}
```

---

## Accessibility Checklist

### Token Design
- [ ] Text/background combinations meet 4.5:1 (AA)
- [ ] UI components meet 3:1 contrast
- [ ] High-contrast theme provides 7:1 (AAA)
- [ ] Focus indicators are clearly visible
- [ ] Reduced motion preference honored

### Implementation
- [ ] Use semantic color tokens (not primitives)
- [ ] Provide focus indicators on all interactive elements
- [ ] Don't rely on color alone (use icons/patterns)
- [ ] Test with colorblind simulators
- [ ] Test keyboard navigation

### Testing Tools
- **Chrome DevTools**: Contrast ratio checker, color vision deficiency simulator
- **Firefox**: Accessibility inspector
- **WAVE**: Web accessibility evaluation tool
- **axe DevTools**: Automated accessibility testing

---

## Resources

- **WCAG 2.1:** https://www.w3.org/WAI/WCAG21/quickref/
- **Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Color Blind Simulator:** Sim Daltonism (Mac), Color Oracle (cross-platform)

---

**Validation script:** `scripts/validate_contrast.py`
