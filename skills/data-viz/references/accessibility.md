# Data Visualization Accessibility Guide (WCAG 2.1 AA)

Ensure all visualizations meet Web Content Accessibility Guidelines Level AA standards.

## Core Requirements

### 1. Text Alternatives (WCAG 1.1.1 - Level A)

**Every visualization needs a text alternative describing the key insight.**

**Simple Charts (one key insight):**
```html
<figure role="img" aria-label="Revenue increased 23% in Q4 2024">
  <svg>...</svg>
</figure>
```

**Complex Charts (multiple insights):**
```html
<figure role="img" aria-labelledby="chart-title" aria-describedby="chart-desc">
  <figcaption id="chart-title">Quarterly Revenue Trends 2024</figcaption>
  <svg>...</svg>

  <!-- Long description for screen readers -->
  <div id="chart-desc" class="sr-only">
    Revenue started at $1.2M in Q1, declined to $1.0M in Q2 due to seasonal factors,
    recovered to $1.3M in Q3 following product launch, and reached $1.5M in Q4,
    representing 23% growth over Q3 and establishing a new company record.
  </div>
</figure>
```

**Screen reader only class:**
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

### 2. Color Contrast (WCAG 1.4.3 - Level AA)

**Minimum contrast ratios:**
- **Non-text content** (chart elements): 3:1
- **Normal text**: 4.5:1
- **Large text** (≥24px or ≥19px bold): 3:1

**Test colors:**
```javascript
// Use WebAIM contrast checker
// https://webaim.org/resources/contrastchecker/

const validateContrast = (foreground, background) => {
  const ratio = calculateContrastRatio(foreground, background);
  return {
    AA_normal: ratio >= 4.5,
    AA_large: ratio >= 3.0,
    AAA_normal: ratio >= 7.0,
  };
};
```

**Chart-specific:**
```
✅ Dark blue (#1E40AF) on white (#FFFFFF): 10.4:1 (Excellent)
✅ Purple (#8B5CF6) on white: 4.86:1 (AA Pass)
⚠️  Yellow (#FCD34D) on white: 1.35:1 (FAIL - don't use)
```

---

### 3. Don't Rely on Color Alone (WCAG 1.4.1 - Level A)

**Use multiple visual cues:**

**Patterns/Textures:**
```tsx
// React example with SVG patterns
<svg>
  <defs>
    {/* Diagonal lines */}
    <pattern id="diagonal" width="4" height="4" patternUnits="userSpaceOnUse">
      <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" stroke="currentColor" strokeWidth="0.5" />
    </pattern>

    {/* Dots */}
    <pattern id="dots" width="4" height="4" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="currentColor" />
    </pattern>

    {/* Grid */}
    <pattern id="grid" width="4" height="4" patternUnits="userSpaceOnUse">
      <path d="M 4 0 L 0 0 0 4" fill="none" stroke="currentColor" strokeWidth="0.5" />
    </pattern>
  </defs>

  <rect x="0" y="0" width="100" height="50" fill="url(#diagonal)" style={{color: '#3B82F6'}} />
  <rect x="0" y="60" width="100" height="50" fill="url(#dots)" style={{color: '#10B981'}} />
  <rect x="0" y="120" width="100" height="50" fill="url(#grid)" style={{color: '#F59E0B'}} />
</svg>
```

**Direct Labels:**
```
Instead of legend only, add labels directly to data:
✅ Each bar labeled with value
✅ Line endpoints labeled with final value
✅ Pie slices labeled with percentage
```

**Shapes + Color:**
```
✅ Use circles for Series A, squares for Series B
✅ Use solid line for Actual, dashed for Forecast
✅ Use different marker shapes in scatter plots
```

---

### 4. Keyboard Navigation (WCAG 2.1.1 - Level A)

**Interactive charts must be keyboard accessible:**

**Requirements:**
- **Tab**: Navigate to chart, then to interactive elements
- **Enter/Space**: Activate tooltips, select data points
- **Arrow Keys**: Navigate between data points
- **Escape**: Close tooltips, exit interaction mode

**Implementation (React + Recharts):**
```tsx
function AccessibleBarChart({ data }) {
  const [focusedIndex, setFocusedIndex] = useState(-1);

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowRight') {
      setFocusedIndex(Math.min(focusedIndex + 1, data.length - 1));
    } else if (e.key === 'ArrowLeft') {
      setFocusedIndex(Math.max(focusedIndex - 1, 0));
    } else if (e.key === 'Enter' || e.key === ' ') {
      // Show tooltip for focused item
      showTooltip(data[focusedIndex]);
    }
  };

  return (
    <div
      tabIndex={0}
      onKeyDown={handleKeyDown}
      role="img"
      aria-label="Revenue by category"
    >
      <BarChart data={data}>
        {/* Chart implementation */}
      </BarChart>
    </div>
  );
}
```

---

### 5. Data Table Alternative

**Provide accessible table view for all charts:**

```tsx
function AccessibleChart({ data }) {
  const [view, setView] = useState('chart'); // or 'table'

  return (
    <div>
      <div role="tablist">
        <button
          role="tab"
          aria-selected={view === 'chart'}
          onClick={() => setView('chart')}
        >
          Chart View
        </button>
        <button
          role="tab"
          aria-selected={view === 'table'}
          onClick={() => setView('table')}
        >
          Table View
        </button>
      </div>

      {view === 'chart' ? (
        <figure role="img" aria-label="Sales trends Q1-Q4">
          <LineChart data={data}>...</LineChart>
        </figure>
      ) : (
        <table>
          <caption>Quarterly Sales Data 2024</caption>
          <thead>
            <tr>
              <th scope="col">Quarter</th>
              <th scope="col">Sales ($)</th>
              <th scope="col">Change (%)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i}>
                <th scope="row">{row.quarter}</th>
                <td>{row.sales.toLocaleString()}</td>
                <td>{row.change > 0 ? '+' : ''}{row.change}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
```

---

### 6. Screen Reader Support

**Announce dynamic updates:**
```tsx
function LiveChart({ data }) {
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  return (
    <div>
      {/* Live region for screen readers */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {isLoading
          ? 'Loading chart data...'
          : lastUpdate
          ? `Chart updated at ${lastUpdate.toLocaleTimeString()}`
          : 'Chart ready'}
      </div>

      <LineChart data={data}>...</LineChart>
    </div>
  );
}
```

**ARIA roles for chart elements:**
```html
<!-- Chart container -->
<div role="img" aria-label="Description">

  <!-- Interactive elements -->
  <button role="button" aria-label="Zoom in">+</button>
  <button role="button" aria-label="Reset zoom">Reset</button>

  <!-- Legend -->
  <div role="list" aria-label="Chart legend">
    <div role="listitem">Series A: Blue solid line</div>
    <div role="listitem">Series B: Red dashed line</div>
  </div>

</div>
```

---

## Testing Checklist

### Automated Testing

**Tools:**
- **axe DevTools** (Chrome/Firefox extension)
- **WAVE** (Web Accessibility Evaluation Tool)
- **Lighthouse** (Chrome DevTools)

**Run automated scans:**
```bash
# Example with axe-core (if integrated)
npm run test:a11y
```

### Manual Testing

**Screen Reader Testing:**
- [ ] Test with NVDA (Windows) or JAWS
- [ ] Test with VoiceOver (Mac/iOS)
- [ ] Test with TalkBack (Android)
- [ ] Verify all content announced correctly
- [ ] Check reading order makes sense

**Keyboard Testing:**
- [ ] Disconnect mouse
- [ ] Tab through all interactive elements
- [ ] Verify focus indicators visible
- [ ] Test all keyboard shortcuts work
- [ ] Ensure no keyboard traps

**Color Vision Testing:**
- [ ] Use browser DevTools color vision emulator
- [ ] Test with Sim Daltonism (Mac) or Color Oracle
- [ ] Verify patterns/labels work without color
- [ ] Check contrast ratios

**Zoom Testing:**
- [ ] Zoom to 200% (WCAG requirement)
- [ ] Verify chart still readable
- [ ] Check responsive behavior
- [ ] Ensure no horizontal scrolling on mobile

---

## Common Accessibility Pitfalls

### ❌ Avoid:

1. **Color-only encoding**
   - Using only color to distinguish categories
   - No patterns, shapes, or labels

2. **Missing text alternatives**
   - Chart without aria-label or description
   - Decorative vs. informative unclear

3. **Low contrast**
   - Pastel colors on white background
   - Light gray text on slightly darker gray

4. **Inaccessible tooltips**
   - Tooltips only on hover (not keyboard)
   - Tooltips disappear too quickly
   - No way to access tooltip content

5. **No keyboard support**
   - Interactive charts mouse-only
   - Can't navigate data points
   - Focus indicators missing

6. **Unlabeled axes**
   - Missing units (%, $, etc.)
   - Abbreviations without explanation
   - No axis titles

### ✅ Do:

1. **Multiple encoding channels**
   - Color + pattern + shape
   - Color + label + legend

2. **Comprehensive text alternatives**
   - Short aria-label for key insight
   - Long description for details
   - Data table for exact values

3. **High contrast**
   - Test all color combinations
   - Use design tokens (auto WCAG compliance)
   - Provide high-contrast theme option

4. **Accessible interactions**
   - Keyboard navigation implemented
   - Tooltips accessible via keyboard
   - Focus indicators clearly visible

5. **Clear labeling**
   - All axes labeled with units
   - Legend with clear icons
   - Direct labels when possible

---

## ARIA Patterns for Charts

### Static Charts

```html
<figure role="img" aria-labelledby="title" aria-describedby="desc">
  <figcaption id="title">Monthly Sales 2024</figcaption>
  <svg><!-- chart --></svg>
  <div id="desc" class="sr-only">
    Sales ranged from $2M to $5M, with peak in December.
  </div>
</figure>
```

### Interactive Charts

```html
<div role="application" aria-label="Interactive sales chart">
  <div role="toolbar" aria-label="Chart controls">
    <button aria-label="Zoom in">+</button>
    <button aria-label="Zoom out">-</button>
    <button aria-label="Reset view">Reset</button>
  </div>

  <svg role="img" aria-label="Chart visualization">
    <!-- Use role="graphics-document" for complex interactive graphics -->
  </svg>

  <!-- Live region for updates -->
  <div role="status" aria-live="polite" aria-atomic="true" class="sr-only">
    <!-- Announces: "Showing data for January 2024" when user interacts -->
  </div>
</div>
```

### Data Points with Landmarks

```html
<!-- For navigable data points -->
<g role="list" aria-label="Data points">
  <circle role="listitem" aria-label="January: 4000 sales" .../>
  <circle role="listitem" aria-label="February: 3000 sales" .../>
  <circle role="listitem" aria-label="March: 5000 sales" .../>
</g>
```

---

## Resources

**Testing Tools:**
- Chrome Lighthouse (automated)
- axe DevTools (automated)
- WAVE (automated + manual)
- NVDA, JAWS, VoiceOver (screen reader testing)
- Color Oracle, Sim Daltonism (colorblind simulation)

**Guidelines:**
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/

**Articles:**
- "Accessible SVG Charts" - Sarah Higley
- "Chartability" - Frank Elavsky (accessibility workbook for charts)

---

*Accessibility is not optional. Every visualization must meet WCAG 2.1 AA standards to ensure all users can access and understand the data.*
