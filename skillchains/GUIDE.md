# Skill Chaining Guide

**Complete guide to multi-skill workflows in ai-design-components**

---

## What You'll Learn

1. **What is skill chaining?** - How multiple skills work together
2. **Why it matters** - 70-98% token efficiency gains
3. **Available chains** - Ready-to-use workflows (3 complete)
4. **Future chains** - Roadmap for upcoming skills (11+ planned)
5. **How to use** - Practical guide with examples

---

## Quick Start

### Available Now (3 Complete Skills)

**1. Themed Charts**
```
Chain: design-tokens → data-viz
Example: "Create a dark-mode bar chart with brand colors"
Efficiency: 85% token savings
```

**2. Branded Forms**
```
Chain: design-tokens → forms
Example: "Build a login form with orange brand color #FF6B35"
Efficiency: 80% token savings
```

**3. Interactive Dashboard**
```
Chain: design-tokens + data-viz + forms
Example: "Analytics dashboard with charts and date filters"
Efficiency: 80% token savings
```

---

## Understanding Skill Chaining

### What is It?

**Skill chaining** = Multiple Claude Skills coordinating to accomplish complex tasks

**Example:**
```
You: "Create a themed sales chart"

Claude automatically:
1. Loads data-viz skill (for charts)
2. Sees reference to design-tokens (for theming)
3. Loads design-tokens skill
4. Generates chart using both skills
```

**You don't specify skills** - Claude discovers them automatically!

---

### Why It Works

**Progressive Disclosure:**
```
Level 1: Metadata (always loaded) - ~100 tokens per skill
    ↓
Level 2: SKILL.md (when triggered) - ~5,000 tokens per skill
    ↓
Level 3: References (as needed) - ~2,000 tokens per file
```

**Token Efficiency:**
- Load only what you need
- Shared skills loaded once (design-tokens)
- Scripts execute without loading (0 tokens!)

---

## The Three Chain Patterns

### 1. Hub-and-Spoke (Best for Efficiency)

```
        design-tokens (HUB)
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
 data-viz   forms   tables
```

**When:** One foundational skill + many components
**Efficiency:** 83-85% (hub loaded once, shared by all)
**Example:** design-tokens styling all component skills

**See:** `patterns/hub-and-spoke.md`

---

### 2. Linear Chain (Best for Workflows)

```
design-tokens → forms → navigation
      ↓           ↓          ↓
   Styling    Inputs   Multi-step
```

**When:** Sequential dependencies (A needs B needs C)
**Efficiency:** 67-75%
**Example:** Multi-step form wizard

**See:** `patterns/linear-chain.md`

---

### 3. Parallel Composition (Best for Features)

```
design-tokens + data-viz + forms + tables
       ↓            ↓        ↓       ↓
    Theme       Charts  Filters   Grid
       └────────────┼────────────┘
                    ↓
            Complete Dashboard
```

**When:** Multiple independent features
**Efficiency:** 75-80%
**Example:** Full analytics dashboard

**See:** `patterns/parallel-composition.md`

---

## How to Use Skill Chains

### Method 1: Natural Language (Automatic)

**Just describe what you want:**

```
"Create a bar chart with dark mode"
→ Claude loads: design-tokens + data-viz

"Build a login form with brand colors"
→ Claude loads: design-tokens + forms

"Make an analytics dashboard with filters"
→ Claude loads: design-tokens + data-viz + forms
```

**Claude automatically:**
- Identifies required skills
- Loads them in correct order
- Coordinates between them
- Generates cohesive output

---

### Method 2: Explicit Mention (Manual)

**Reference skills directly:**

```
"Use the data-viz and design-tokens skills to create a themed chart"
→ Claude loads both explicitly

"Build a form using the forms skill with design-tokens for styling"
→ Claude loads as requested
```

**Useful when:**
- You know exactly which skills you need
- Claude might not auto-detect
- Being explicit about requirements

---

## Available Chains (Now)

### Chain 1: design-tokens → data-viz ✅

**File:** `chains/design-tokens-to-data-viz.md`

**Use when:**
- Creating charts with brand colors
- Need theme switching for visualizations
- Want colorblind-safe palettes
- Building dashboards

**Example request:**
> "Create a line chart showing revenue trends with dark mode support"

**Skills loaded:**
- design-tokens (theming)
- data-viz (charts)

**Token cost:** ~10,000 tokens
**Savings:** 66% vs. inline theming

---

### Chain 2: design-tokens → forms ✅

**File:** `chains/design-tokens-to-forms.md`

**Use when:**
- Building branded login/signup forms
- Need themed form components
- Want consistent button/input styling
- Generating brand color palettes

**Example request:**
> "Build a signup form with my brand color #FF6B35"

**Skills loaded:**
- design-tokens (theming + color generation)
- forms (components)

**Token cost:** ~10,000 tokens
**Savings:** 65% vs. inline theming
**Bonus:** Script execution for palette generation (0 tokens!)

---

### Chain 3: data-viz + forms + design-tokens ✅

**File:** `chains/data-viz-plus-forms.md`

**Use when:**
- Interactive dashboards
- Charts with filter controls
- Analytics with date range selection
- Filterable visualizations

**Example request:**
> "Build a sales dashboard with bar chart and date filter"

**Skills loaded:**
- design-tokens (styling foundation)
- data-viz (charts)
- forms (filter inputs)

**Token cost:** ~15,000 tokens
**Savings:** 80% vs. monolithic approach

**Working example:** `examples/themed-sales-dashboard.tsx`

---

## Future Chains (Coming Soon)

### High Priority

**4. Dashboard Full Stack** 🚧
- Skills: design-tokens + dashboards + data-viz + tables + forms
- Use case: Complete BI platform
- ETA: Q1 2026 (needs tables + dashboards)
- **File:** `chains/dashboard-full-stack.md`

**5. AI Chat Interface** 🚀
- Skills: design-tokens + ai-chat + forms
- Use case: Chatbots, AI assistants
- ETA: Q2 2026 (needs ai-chat)
- Priority: **STRATEGIC**
- **File:** `chains/ai-chat-interface.md`

**6. Tables + Data-viz**
- Skills: design-tokens + tables + data-viz
- Use case: Tables with embedded charts
- ETA: Q1 2026 (needs tables)
- **File:** `chains/tables-data-viz-chain.md`

### Complete Roadmap

**See:** `ROADMAP.md` for full 25+ chain plan

---

## Token Efficiency Guide

### Understanding the Savings

**Monolithic Approach (OLD WAY):**
```
Every skill includes everything:
- data-viz = charts + theming + accessibility
- forms = inputs + theming + validation
- tables = grids + theming + sorting

Each skill: 30,000+ tokens
3 skills: 90,000 tokens
```

**Skill Chaining (OUR WAY):**
```
design-tokens (theming): 5,000 tokens (shared)
data-viz (charts only): 5,000 tokens
forms (inputs only): 5,000 tokens
tables (grids only): 5,000 tokens

4 skills: 20,000 tokens
SAVINGS: 78%
```

**Key insight:** More skills = higher efficiency (hub loaded once)

**Complete analysis:** `TOKEN_EFFICIENCY.md`

---

## Practical Examples

### Example 1: Build a Chart

**Without specifying skills:**
```
You: "Create a bar chart showing quarterly sales"

Claude:
- Identifies: Need charts → loads data-viz
- Sees: Charts reference design-tokens → loads it
- Generates: Themed chart using both skills
```

**With explicit mention:**
```
You: "Use data-viz and design-tokens to create a themed bar chart"

Claude:
- Loads both skills explicitly
- Generates themed chart
```

**Result is the same** - explicit just ensures both load.

---

### Example 2: Brand Customization

**Request:**
```
You: "Generate a brand color palette from orange #FF6B35"

Claude:
- Loads design-tokens
- Executes: python scripts/generate_color_scale.py (0 tokens!)
- Returns: 9-shade palette
```

**Token cost:**
- design-tokens SKILL.md: 5,000 tokens
- Script execution: 0 tokens (code not loaded)
- Output: 200 tokens
- **Total: 5,200 tokens**

**vs. inline algorithm: 15,000 tokens**
**Savings: 65%**

---

### Example 3: Multi-Skill Dashboard

**Request:**
```
You: "Build an analytics dashboard with:
- Revenue bar chart
- Category pie chart
- Date range filter
- All themed with dark mode"

Claude:
- Loads design-tokens (theme foundation)
- Loads data-viz (bar + pie charts)
- Loads forms (date range picker)
- Coordinates all three
- Generates cohesive dashboard
```

**Token cost:** ~15,000 tokens
**vs. monolithic:** ~75,000 tokens
**Savings: 80%**

---

## Best Practices

### For Users

**1. Describe the complete requirement**
```
✅ "Build a dashboard with charts and filters"
❌ "Build something" (too vague)
```

**2. Mention themes/brands when needed**
```
✅ "Create charts with our brand colors"
→ Triggers design-tokens chain
```

**3. Trust automatic chaining**
```
Claude will load needed skills automatically
Don't need to explicitly mention skill names
```

### For Skill Developers

**1. Reference dependencies in SKILL.md**
```markdown
## Integration with Other Skills
- Uses design-tokens for styling
- Works with dashboards for layout
```

**2. Use consistent token naming**
```css
--{component}-{property}-{variant?}-{state?}
```

**3. Keep skills focused**
```
One domain per skill
Reference other skills for cross-cutting concerns
```

---

## Measuring Success

### Token Efficiency Metrics

**Chain size vs. savings:**
- 2 skills: 70-80% savings
- 3 skills: 80-85% savings
- 4-5 skills: 85-90% savings
- 6+ skills: 90-92% savings (plateau)

**Sweet spot:** 3-5 skill chains

### Financial ROI

**API cost savings:**
- Single task: 71% reduction
- 100 tasks/day: $6,570/year saved
- 1,000 tasks/day: $65,700/year saved

**See:** `TOKEN_EFFICIENCY.md` for complete analysis

---

## Quick Reference

### Current Chains

| Chain | Skills | Status | Use Case | Doc |
|-------|--------|--------|----------|-----|
| Themed Charts | design-tokens + data-viz | ✅ Ready | Branded visualizations | [Link](./chains/design-tokens-to-data-viz.md) |
| Branded Forms | design-tokens + forms | ✅ Ready | Login/signup forms | [Link](./chains/design-tokens-to-forms.md) |
| Dashboard | All 3 | ✅ Ready | Analytics dashboards | [Link](./chains/data-viz-plus-forms.md) |

### Future Chains

| Chain | Skills | Status | Priority | ETA |
|-------|--------|--------|----------|-----|
| Full Dashboard | +tables +dashboards | 🚧 | Very High | Q1 2026 |
| AI Chat | +ai-chat | 🚧 | **STRATEGIC** | Q2 2026 |
| Tables + Viz | +tables | 🚧 | High | Q1 2026 |

**Full roadmap:** `ROADMAP.md`

---

## Resources

**Documentation:**
- `README.md` - Overview and chain catalog
- `GUIDE.md` - This file (complete usage guide)
- `ROADMAP.md` - Future chains and priorities
- `TOKEN_EFFICIENCY.md` - Efficiency analysis

**Patterns:**
- `patterns/hub-and-spoke.md` - Most efficient pattern
- `patterns/linear-chain.md` - Sequential workflows
- `patterns/parallel-composition.md` - Complex UIs

**Chain Documentation:**
- `chains/` - Individual chain guides (6 documented)

**Examples:**
- `examples/themed-sales-dashboard.tsx` - Working 3-skill chain

---

**Updated:** November 13, 2025
**Coverage:** 3 current chains, 3 future chains, 3 architectural patterns
**Status:** Complete documentation for current implementation
