# Color Systems for Data Visualization

Comprehensive guide to color usage in charts.


## Table of Contents

- [Color Scale Types](#color-scale-types)
  - [1. Categorical (Qualitative)](#1-categorical-qualitative)
  - [2. Sequential (Single-Hue)](#2-sequential-single-hue)
  - [3. Diverging (Two-Hue)](#3-diverging-two-hue)
- [Colorblind Considerations](#colorblind-considerations)
  - [Types of Colorblindness](#types-of-colorblindness)
  - [Colorblind-Safe Strategies](#colorblind-safe-strategies)
- [Testing Tools](#testing-tools)
- [WCAG Contrast Requirements](#wcag-contrast-requirements)
- [Color Palette Selection Guide](#color-palette-selection-guide)
  - [For Business Dashboards](#for-business-dashboards)
  - [For Scientific Publications](#for-scientific-publications)
  - [For Financial Charts](#for-financial-charts)
  - [For Geographic/Heatmaps](#for-geographicheatmaps)
  - [For Correlation Matrices](#for-correlation-matrices)
- [Implementation Examples](#implementation-examples)
  - [Using Categorical Palette (React)](#using-categorical-palette-react)
  - [Using Sequential Scale (Python)](#using-sequential-scale-python)
  - [Using Diverging Scale (D3)](#using-diverging-scale-d3)
- [Design Token Integration](#design-token-integration)

## Color Scale Types

### 1. Categorical (Qualitative)
**Purpose:** Distinguish different categories (no inherent order)
**Use for:** Product lines, regions, categories
**Max categories:** 10 (human limit for distinguishing colors)

**Recommendations:**
- IBM Colorblind-Safe (5 colors) - Primary choice
- Paul Tol Qualitative (7 colors) - Scientific
- D3 Category10 - Standard web

**Asset:** `assets/color-palettes/colorblind-safe.json`

---

### 2. Sequential (Single-Hue)
**Purpose:** Show magnitude/intensity (low to high)
**Use for:** Heatmaps, choropleths, intensity maps
**Range:** Light → Dark (or vice versa)

**Recommendations:**
- Blues: #EFF6FF → #1E3A8A
- Greens: #F0FDF4 → #14532D
- Reds: #FEF2F2 → #7F1D1D

**Properties:**
- Perceptually uniform (equal visual steps)
- Monotonically increasing lightness
- Single hue for clarity

**Asset:** `assets/color-palettes/sequential-scales.json`

---

### 3. Diverging (Two-Hue)
**Purpose:** Show deviation from midpoint (negative/positive)
**Use for:** Profit/loss, temperature anomalies, correlation matrices
**Range:** Color A ← Neutral → Color B

**Recommendations:**
- Red-Blue: Negative (red) ← Gray → Positive (blue)
- Orange-Blue: Colorblind-safe alternative
- Purple-Green: Alternative pairing

**Critical:** Avoid red-green (8% of males are red-green colorblind)

**Asset:** `assets/color-palettes/diverging-scales.json`

---

## Colorblind Considerations

### Types of Colorblindness

**Deuteranopia** (most common, ~5% of males)
- Reduced sensitivity to green
- Red/green confusion

**Protanopia** (~2.5% of males)
- Reduced sensitivity to red
- Red/green confusion

**Tritanopia** (rare, <0.01%)
- Reduced sensitivity to blue
- Blue/yellow confusion

**Achromatopsia** (very rare)
- Complete color blindness
- See only grayscale

---

### Colorblind-Safe Strategies

**1. Use Tested Palettes**
- IBM palette (5 colors) - Safe for all types
- Paul Tol palette (7 colors) - Scientific standard
- Wong palette (8 colors) - Nature Methods recommended

**2. Avoid Problem Combinations**
- ❌ Red + Green (deuteranopia/protanopia can't distinguish)
- ❌ Blue + Purple (can be hard to distinguish)
- ✅ Blue + Orange (high contrast, safe)
- ✅ Blue + Yellow (high contrast, safe)

**3. Add Non-Color Cues**
- Patterns/textures
- Shapes (circles vs. squares)
- Labels (direct labeling)
- Line styles (solid vs. dashed)

---

## Testing Tools

**Browser DevTools:**
- Chrome: DevTools → Rendering → Emulate vision deficiencies
- Firefox: Accessibility Inspector

**Desktop Apps:**
- **Sim Daltonism** (Mac) - Real-time simulation
- **Color Oracle** (Windows/Mac/Linux) - Full-screen simulation

**Online:**
- Coblis Color Blindness Simulator
- WebAIM Contrast Checker

**Testing Script:**
```bash
# Validate chart colors
python scripts/validate_accessibility.py chart.html
```

---

## WCAG Contrast Requirements

**Minimum Ratios:**
- **Non-text (UI elements):** 3:1 (Level AA)
- **Normal text:** 4.5:1 (Level AA)
- **Large text** (≥24px or ≥19px bold): 3:1 (Level AA)

**Enhanced (Level AAA):**
- Normal text: 7:1
- Large text: 4.5:1

**Examples:**
```
✅ Dark blue (#1E40AF) on white (#FFFFFF): 10.4:1 (AAA)
✅ Purple (#8B5CF6) on white: 4.86:1 (AA normal text)
✅ Orange (#F59E0B) on white: 3.95:1 (AA large text only)
❌ Yellow (#FCD34D) on white: 1.35:1 (FAIL)
```

---

## Color Palette Selection Guide

### For Business Dashboards
**Use:** IBM Colorblind-Safe or Default 10-Color
**Why:** Professional, accessible, works for most users

### For Scientific Publications
**Use:** Paul Tol Qualitative or Viridis (sequential)
**Why:** Perceptually uniform, print-friendly

### For Financial Charts
**Use:** Red-Blue diverging (profit/loss)
**Why:** Industry convention

### For Geographic/Heatmaps
**Use:** Sequential single-hue (Blues, Greens)
**Why:** Magnitude clear, no confusion

### For Correlation Matrices
**Use:** Red-Blue or Orange-Blue diverging
**Why:** Negative/neutral/positive clear

---

## Implementation Examples

### Using Categorical Palette (React)
```tsx
import palette from '../assets/color-palettes/colorblind-safe.json';

const IBM_COLORS = palette.ibm.colors.map(c => c.hex);

<Bar dataKey="value" fill={IBM_COLORS[0]} />
```

### Using Sequential Scale (Python)
```python
import json
import plotly.graph_objects as go

with open('assets/color-palettes/sequential-scales.json') as f:
    palettes = json.load(f)

blues = [c['hex'] for c in palettes['blues']['colors']]

fig = go.Figure(data=go.Heatmap(
    z=data,
    colorscale=list(zip(
        [i/(len(blues)-1) for i in range(len(blues))],
        blues
    ))
))
```

### Using Diverging Scale (D3)
```javascript
import * as d3 from 'd3';
import diverging from '../assets/color-palettes/diverging-scales.json';

const negColors = diverging.redBlue.negative.map(c => c.hex);
const posColors = diverging.redBlue.positive.map(c => c.hex);
const midColor = diverging.redBlue.midpoint.hex;

const colorScale = d3.scaleSequential()
  .domain([-5, 5])
  .interpolator(d3.interpolateRdBu);  // Or custom scale from JSON
```

---

## Design Token Integration

**Use design tokens for chart colors:**
```css
/* Define in design tokens */
--chart-color-primary: #3B82F6;
--chart-color-success: #10B981;
--chart-color-warning: #F59E0B;
--chart-color-error: #EF4444;

/* Reference in charts */
<Bar fill="var(--chart-color-primary)" />
```

**Benefits:**
- Theme switching (light/dark)
- Brand customization
- Consistent across all charts

**See:** `../design-tokens/` skill for complete token system

---

*Color is a powerful encoding channel, but must be used responsibly. Always test for colorblindness and provide non-color alternatives.*
