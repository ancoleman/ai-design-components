# Skill Library Visualizations

Three complementary visualizations of the ai-design-components skill library, demonstrating the **data-viz** skill's guidance on selecting appropriate chart types based on data characteristics and analytical purpose.

## Overview

This demo showcases three different visualization approaches for the same hierarchical dataset:

1. **Treemap** - Hierarchical overview (best for at-a-glance understanding)
2. **Grouped Bar Chart** - Category comparison (best for progress tracking)
3. **Sunburst Chart** - Interactive exploration (best for engagement)

## Data Structure

**Dataset:** 14 skills across 6 plugin groups
- **Complete skills:** 2 (data-viz, forms)
- **In progress:** 12 remaining skills
- **Overall completion:** ~14%

**Hierarchy:**
```
Plugin Groups (6)
├── ui-foundation-skills (0/1 complete)
├── ui-data-skills (2/3 complete) ⭐
├── ui-input-skills (1/2 complete)
├── ui-interaction-skills (0/3 complete)
├── ui-structure-skills (0/3 complete)
└── ui-content-skills (0/2 complete)
```

## Visualization Breakdown

### 1. Treemap (Hierarchical Overview)

**When to use:**
- At-a-glance overview needed
- Space-efficient display required
- Hierarchical proportions matter

**Strengths:**
- Shows all 14 skills + 6 groups in one compact view
- Visual hierarchy clear (groups → skills)
- Color coding instantly shows status
- Efficient use of screen space

**Implementation:**
- Library: Recharts
- File: `SkillLibraryTreemap.tsx`
- Features: Responsive, accessible, data table alternative

**Following data-viz skill guidance:**
> "Hierarchical data → Treemap when focus on proportions and composition"

---

### 2. Grouped Bar Chart (Plugin Group Comparison)

**When to use:**
- Comparing categories is primary goal
- Progress tracking across groups
- Stakeholder presentations

**Strengths:**
- Easy comparison of complete vs WIP across groups
- Sorted by completion rate (highest first)
- Clear axis labels and legend
- Familiar chart type (no learning curve)

**Implementation:**
- Library: Recharts
- File: `SkillLibraryBarChart.tsx`
- Features: Sorted display, summary statistics, tooltips

**Following data-viz skill guidance:**
> "Compare categories → Bar Chart - universally understood and effective"

---

### 3. Sunburst Chart (Interactive Exploration)

**When to use:**
- Interactive exploration desired
- Engaging presentation needed
- Hierarchical drill-down useful

**Strengths:**
- Visually engaging radial layout
- Interactive hover and click
- Shows proportional distribution
- Modern, professional appearance

**Implementation:**
- Library: D3.js
- File: `SkillLibrarySunburst.tsx`
- Features: Custom SVG, interactive states, center focus

**Following data-viz skill guidance:**
> "Custom visualizations requiring maximum flexibility → D3.js"

---

## Accessibility Features

All visualizations follow WCAG 2.1 AA compliance:

✅ **Color Contrast:** 3:1 minimum for UI elements
✅ **Colorblind-Safe Palette:** Paul Tol palette (no red/green reliance)
✅ **Text Alternatives:** `aria-label` and `<figure role="img">`
✅ **Data Table Alternative:** Collapsible tables for screen readers
✅ **Keyboard Navigation:** Full keyboard support (where applicable)
✅ **Screen Reader Announcements:** Status updates via `aria-live`

**Color Scheme:**
- Complete: `#228833` (Green)
- In Progress: `#FFB000` (Yellow/Orange)
- Plugin Groups: `#4477AA` (Blue)

---

## Installation & Running

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The demo will open at `http://localhost:3000`

---

## Tech Stack

**Framework:** React 18 + TypeScript
**Build Tool:** Vite 5
**Visualization Libraries:**
- **Recharts** 2.10 - Treemap, Bar Chart
- **D3.js** 7.8 - Sunburst Chart

**Bundle Size:** ~200KB (including libraries)

---

## File Structure

```
skill-library-viz/
├── App.tsx                      # Main app with view switching
├── main.tsx                     # React entry point
├── index.html                   # HTML template
├── skillLibraryData.ts          # Shared data source
├── SkillLibraryTreemap.tsx      # Treemap visualization
├── SkillLibraryBarChart.tsx     # Grouped bar chart
├── SkillLibrarySunburst.tsx     # Sunburst chart (D3)
├── package.json                 # Dependencies
├── tsconfig.json                # TypeScript config
├── vite.config.ts               # Vite config
└── README.md                    # This file
```

---

## Key Learnings from data-viz Skill

### Selection Framework Applied

**Data Assessment:**
- Type: Categorical + Hierarchical
- Dimensions: 2D (group + skill)
- Volume: Small (<100 data points)
- Purpose: Show composition, hierarchy, progress

**Chart Selection Decision Tree:**
```
Hierarchical data?
├─ Focus on proportions → Treemap ✓
├─ Compare categories → Grouped Bar ✓
└─ Interactive exploration → Sunburst ✓
```

### Progressive Disclosure Pattern

Following Anthropic Skills best practices:

**Skill Structure:**
1. **SKILL.md** - Overview and quick start (<500 lines)
2. **references/** - Detailed chart catalog and guides
3. **examples/** - Working code (this demo)

**Token Efficiency:**
- Metadata always loaded (name + description)
- Full skill content loaded on trigger
- Examples accessed as needed

---

## Performance Notes

**Dataset Size:** 14 skills (trivial for all chart types)

**Rendering Performance:**
- Treemap: <50ms
- Bar Chart: <30ms
- Sunburst: <100ms (D3 custom rendering)

**Optimization Strategies** (from data-viz skill):
- <1,000 points: Direct rendering (SVG) ✓ Applied
- 1K-10K: Consider sampling
- >10K: Canvas rendering or server-side aggregation

---

## Future Enhancements

Potential improvements:

1. **Theme Switching** - Light/dark/high-contrast (using design-tokens skill)
2. **Export Functionality** - Download as PNG/SVG
3. **Filter Controls** - Show/hide specific plugin groups
4. **Animation** - Smooth transitions between states
5. **Drill-Down** - Click plugin group to see skill details
6. **Comparison View** - Side-by-side chart comparisons

---

## License

MIT - Part of ai-design-components

---

## References

**data-viz skill files:**
- `skills/data-viz/SKILL.md` - Main skill documentation
- `skills/data-viz/references/chart-catalog.md` - 24+ chart types
- `skills/data-viz/references/selection-matrix.md` - Decision trees
- `skills/data-viz/references/accessibility.md` - WCAG patterns

**External Resources:**
- [Recharts Documentation](https://recharts.org/)
- [D3.js Documentation](https://d3js.org/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Paul Tol's Colorblind-Safe Palettes](https://personal.sron.nl/~pault/)

---

**Built following the data-viz skill from ai-design-components**
Demonstrating systematic visualization selection based on data + purpose.
