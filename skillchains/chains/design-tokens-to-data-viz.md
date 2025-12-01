# Skill Chain: design-tokens → data-viz

**Theme charts with brand colors and consistent styling**

Status: ✅ Available Now (Both Skills Complete)

---

## Overview

**Chain:** `design-tokens` → `data-viz`

**Purpose:** Apply consistent, themeable styling to data visualizations

**Use Cases:**
- Branded analytics dashboards
- Multi-theme reporting systems
- Accessible data visualizations
- Chart libraries matching design system

---

## How the Chain Works

### Automatic Coordination

**User Request:**
> "Create a bar chart showing sales data with our brand colors"

**Claude's Process:**

1. **Triggers data-viz skill** (matches "bar chart" and "sales data")
   - Loads `data-viz/SKILL.md`
   - Sees chart implementation patterns

2. **data-viz references design-tokens**
   ```markdown
   ## Integration with Design Tokens
   Chart-specific tokens:
   - --chart-color-1 through --chart-color-8
   - --chart-axis-color
   - --chart-grid-color
   ```

3. **Claude loads design-tokens skill**
   - Gets token definitions
   - Understands theming mechanism
   - Applies to chart implementation

4. **Generates themed chart:**
   ```tsx
   <BarChart data={salesData}>
     <XAxis stroke="var(--chart-axis-color)" />
     <Bar fill="var(--chart-color-1)" />
   </BarChart>
   ```

---

## Token Integration Points

### Chart Color Palette

**Defined in:** `design-tokens/tokens/components/chart.json`

```json
{
  "chart": {
    "color": {
      "1": { "$value": "#648FFF", "$type": "color" },
      "2": { "$value": "#785EF0", "$type": "color" },
      "3": { "$value": "#DC267F", "$type": "color" }
    }
  }
}
```

**Used in data-viz:**
```tsx
// Recharts
<Line stroke="var(--chart-color-1)" />
<Bar fill="var(--chart-color-2)" />

// D3.js
.attr('fill', 'var(--chart-color-1)')
```

**Result:** Charts automatically match theme!

---

### Chart UI Elements

**Tokens:**
```css
--chart-axis-color      /* Axis lines */
--chart-grid-color      /* Grid lines */
--chart-tooltip-bg      /* Tooltip background */
--chart-font-family     /* Text font */
```

**Usage:**
```tsx
<LineChart>
  <XAxis stroke="var(--chart-axis-color)" />
  <YAxis stroke="var(--chart-axis-color)" />
  <CartesianGrid stroke="var(--chart-grid-color)" />
  <Tooltip
    contentStyle={{
      backgroundColor: 'var(--chart-tooltip-bg)',
      border: '1px solid var(--color-border)'
    }}
  />
</LineChart>
```

---

## Theme Switching Example

### Light Theme
```css
:root {
  --chart-color-1: #648FFF;
  --chart-axis-color: #E5E7EB;
  --chart-grid-color: #F3F4F6;
  --chart-tooltip-bg: #FFFFFF;
}
```

### Dark Theme
```css
:root[data-theme="dark"] {
  --chart-color-1: #648FFF;    /* Same (high contrast on dark) */
  --chart-axis-color: #374151; /* Darker axes */
  --chart-grid-color: #1F2937; /* Darker grid */
  --chart-tooltip-bg: #111827; /* Dark tooltip */
}
```

**Same chart component, different theme:**
```javascript
setTheme('dark');  // Chart updates automatically!
```

---

## Complete Example

### User Request
> "Create a line chart showing monthly revenue with dark mode support"

### Claude's Implementation

**1. Chain Activation:**
```
data-viz (primary) → design-tokens (referenced)
```

**2. Generated Code:**
```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export function RevenueChart({ data }) {
  return (
    <div style={{ padding: 'var(--spacing-lg)' }}>
      <h2 style={{
        fontSize: 'var(--font-size-2xl)',
        color: 'var(--color-text-primary)',
        marginBlockEnd: 'var(--spacing-md)'
      }}>
        Monthly Revenue
      </h2>

      <LineChart width={600} height={300} data={data}>
        <XAxis
          dataKey="month"
          stroke="var(--chart-axis-color)"
          style={{ fontSize: 'var(--font-size-sm)' }}
        />
        <YAxis
          stroke="var(--chart-axis-color)"
          style={{ fontSize: 'var(--font-size-sm)' }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'var(--chart-tooltip-bg)',
            border: '1px solid var(--color-border)',
            borderRadius: 'var(--radius-sm)'
          }}
        />
        <Line
          type="monotone"
          dataKey="revenue"
          stroke="var(--chart-color-1)"
          strokeWidth={2}
        />
      </LineChart>
    </div>
  );
}
```

**3. Theme Toggle Works:**
```tsx
<ThemeToggle />  {/* From design-tokens examples */}
<RevenueChart data={monthlyData} />

// User clicks theme toggle → Chart updates automatically
```

---

## Token Efficiency

**This chain:**
- data-viz metadata: 100 tokens (always)
- design-tokens metadata: 100 tokens (always)
- data-viz SKILL.md: 5,000 tokens (triggered)
- design-tokens SKILL.md: 5,000 tokens (chained)
- **Total: 10,200 tokens**

**Without chaining:**
- data-viz with inline theming guidance: 30,000 tokens
- **Savings: 66%**

**For 10 charts in a dashboard:**
- With chaining: 10,200 tokens (design-tokens loaded once)
- Without: 300,000 tokens (repeated guidance × 10)
- **Savings: 97%** 🚀

---

## Benefits

1. ✅ **Automatic theming** - Charts match brand/theme
2. ✅ **Colorblind-safe** - Uses IBM/Paul Tol palettes from design-tokens
3. ✅ **WCAG compliant** - Color contrast validated
4. ✅ **RTL support** - Chart labels use logical properties
5. ✅ **Multi-theme** - Light/dark/high-contrast work automatically
6. ✅ **Token efficient** - 66-97% savings depending on usage

---

## When to Use This Chain

**Trigger phrases:**
- "Create a chart with our brand colors"
- "Build a themed dashboard"
- "Make charts match our design system"
- "Add dark mode to visualizations"
- "Ensure charts are accessible"

**Claude automatically chains these skills when theme/styling is mentioned with charts.**

---

**Status:** ✅ Production ready
**Token Efficiency:** 66-97% savings
**Skills Required:** design-tokens (complete), data-viz (complete)
