# Parallel Composition Pattern

**Multiple independent skills working together (A + B + C)**

---

## Pattern Structure

```
     Skill A    Skill B    Skill C
        ↓          ↓          ↓
        └──────────┼──────────┘
                   ↓
            Combined Output
```

**Characteristics:**
- Skills work independently
- No direct dependencies between skills
- Claude coordinates composition
- Higher token cost (all skills load)

---

## Example: Complex Dashboard

```
data-viz + forms + tables
   ↓        ↓       ↓
Charts  Filters  Grid
   └───────┼───────┘
           ↓
    Full Dashboard
```

**All skills loaded in parallel:**
- No skill depends on another
- Each provides independent functionality
- Claude assembles into cohesive UI

---

## Token Flow

```
User: "Build a dashboard with charts, data tables, and filter controls"

Claude analyzes:
- "charts" → data-viz skill needed
- "data tables" → tables skill needed
- "filter controls" → forms skill needed

Claude loads ALL THREE in parallel:
├─ data-viz SKILL.md (5,000 tokens)
├─ forms SKILL.md (5,000 tokens)
└─ tables SKILL.md (5,000 tokens)

TOTAL: 15,000 tokens
```

**Plus shared hub (if referenced):**
```
+ design-tokens SKILL.md (5,000 tokens)
  └─ All three reference for styling

TOTAL: 20,000 tokens
```

---

## Real-World Example: Analytics Dashboard

### User Request
> "Build an analytics dashboard with:
> - Monthly revenue bar chart
> - Product sales data table
> - Date range and category filters"

### Skills Required

**Parallel composition:**
```
design-tokens (foundation - loaded first)
    ↓
┌───────────┼────────────┐
↓           ↓            ↓
data-viz   tables      forms
```

**Each provides:**
- **data-viz:** Bar chart component
- **tables:** Data grid with sorting
- **forms:** Date picker + category dropdown
- **design-tokens:** Styling for all three

---

### Generated Implementation

```tsx
import { BarChart, Bar, XAxis, YAxis } from 'recharts';
import { DataTable } from './components/DataTable';
import { DateRangePicker } from './components/DateRangePicker';

export function AnalyticsDashboard() {
  const [filters, setFilters] = useState({
    startDate: '2025-01-01',
    endDate: '2025-12-31',
    category: 'all'
  });

  return (
    <div style={{
      padding: 'var(--spacing-xl)',
      backgroundColor: 'var(--color-bg-primary)'
    }}>
      {/* Filter Controls (forms skill) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 'var(--spacing-md)',
        marginBlockEnd: 'var(--spacing-xl)',
        padding: 'var(--spacing-md)',
        backgroundColor: 'var(--color-bg-secondary)',
        borderRadius: 'var(--radius-lg)'
      }}>
        <DateRangePicker
          startDate={filters.startDate}
          endDate={filters.endDate}
          onChange={(start, end) => setFilters({...filters, startDate: start, endDate: end})}
        />

        <select
          value={filters.category}
          onChange={(e) => setFilters({...filters, category: e.target.value})}
          style={{
            height: 'var(--input-height)',
            paddingInline: 'var(--input-padding-inline)',
            backgroundColor: 'var(--input-bg)',
            border: '1px solid var(--input-border-color)',
            borderRadius: 'var(--radius-md)'
          }}
        >
          <option value="all">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
        </select>

        <button
          onClick={applyFilters}
          style={{
            backgroundColor: 'var(--button-bg-primary)',
            color: 'var(--button-text-primary)',
            paddingInline: 'var(--button-padding-inline)',
            borderRadius: 'var(--button-border-radius)'
          }}
        >
          Apply Filters
        </button>
      </div>

      {/* Chart (data-viz skill) */}
      <div style={{
        marginBlockEnd: 'var(--spacing-xl)',
        padding: 'var(--spacing-lg)',
        backgroundColor: 'var(--color-bg-primary)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-md)'
      }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Monthly Revenue
        </h2>

        <BarChart width={800} height={300} data={filteredData}>
          <XAxis dataKey="month" stroke="var(--chart-axis-color)" />
          <YAxis stroke="var(--chart-axis-color)" />
          <Bar dataKey="revenue" fill="var(--chart-color-1)" />
        </BarChart>
      </div>

      {/* Data Table (tables skill) */}
      <div style={{
        padding: 'var(--spacing-lg)',
        backgroundColor: 'var(--color-bg-primary)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-md)'
      }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Product Sales
        </h2>

        <DataTable
          columns={columns}
          data={filteredData}
          // Uses table tokens from design-tokens
        />
      </div>
    </div>
  );
}
```

---

## Token Efficiency

**Parallel composition (4 skills):**
```
design-tokens: 5,000 tokens (hub, loaded once)
data-viz: 5,000 tokens
forms: 5,000 tokens
tables: 5,000 tokens
TOTAL: 20,000 tokens
```

**Without skill chaining:**
```
Each skill with inline theming: 25,000 tokens × 3 = 75,000 tokens
design-tokens separately: 5,000 tokens
TOTAL: 80,000 tokens

SAVINGS: 75%
```

---

## Coordination Complexity

**Claude must:**
1. Identify all required skills from user request
2. Load all skills (may reference each other)
3. Coordinate styling (via design-tokens hub)
4. Generate cohesive UI that feels unified

**Example coordination:**
```
User mentions: "charts" + "tables" + "filters"

Claude:
├─ Loads data-viz (charts)
├─ Loads tables (data grid)
├─ Loads forms (filters)
└─ Sees all reference design-tokens → loads it as hub

All four coordinate:
- Same spacing tokens → consistent padding
- Same color tokens → visual harmony
- Same radius tokens → matching corners
- Same shadow tokens → unified elevation
```

---

## When to Use Parallel Composition

**Use when:**
- ✅ Complex UI requiring multiple independent features
- ✅ No direct dependency between component skills
- ✅ All skills share a common foundation (hub)
- ✅ Building comprehensive applications

**Examples:**
- Dashboard (charts + tables + filters + navigation)
- Admin panel (forms + tables + feedback + media)
- Content editor (forms + media + drag-drop + timeline)

**Don't use when:**
- Simple UI (use single skill)
- Sequential workflow (use linear chain)
- Just need styling (use hub reference only)

---

## Benefits

1. ✅ **Feature richness** - Combine multiple capabilities
2. ✅ **Cohesive UX** - Shared design-tokens ensure consistency
3. ✅ **Token efficient** - Hub loaded once, shared by all
4. ✅ **Modular** - Each skill focuses on one domain

---

## Limitations

### Higher Token Cost
- All skills load (no progressive loading)
- Best for complex UIs that genuinely need all features

### Coordination Overhead
- Claude must understand how skills interact
- May need to clarify integration points

---

**Best for:** Complex applications requiring multiple independent features
**Efficiency:** Good (75% savings with hub)
**Complexity:** High
**Current Support:** Partially (data-viz + forms complete, tables WIP)
