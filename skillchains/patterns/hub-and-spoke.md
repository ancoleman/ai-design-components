# Hub-and-Spoke Pattern

**One foundational skill (hub) referenced by multiple component skills (spokes)**

---

## Pattern Structure

```
           design-tokens (HUB)
                  ↓
        ┌─────────┼─────────┐
        ↓         ↓         ↓
    data-viz   forms    tables
     (spoke)   (spoke)  (spoke)
```

**Characteristics:**
- One central "hub" skill provides shared functionality
- Multiple "spoke" skills reference the hub
- Hub loaded once, benefits all spokes
- Maximum token efficiency

---

## Why This Pattern?

**Problem without hub:**
```
Each skill includes theming guidance:
- data-viz: 30,000 tokens (chart impl + theming)
- forms: 25,000 tokens (forms impl + theming)
- tables: 28,000 tokens (tables impl + theming)
TOTAL: 83,000 tokens

Repeated knowledge: ~45,000 tokens wasted!
```

**Solution with hub:**
```
design-tokens (hub): 5,000 tokens (loaded once)
data-viz (spoke): 5,000 tokens (references hub)
forms (spoke): 5,000 tokens (references hub)
tables (spoke): 5,000 tokens (references hub)
TOTAL: 20,000 tokens

SAVINGS: 76%
```

---

## Real-World Example: design-tokens as Hub

### Hub (design-tokens)

**Provides:**
- Color system (primitives, semantic, component tokens)
- Spacing scale
- Typography system
- Border/radius tokens
- Shadow tokens
- Motion tokens
- Theme switching mechanism
- RTL support via logical properties

**Referenced by ALL component skills**

### Spokes (Component Skills)

**data-viz:**
```markdown
## Styling & Theming
Uses design-tokens for chart colors, axis styling, tooltips.

Tokens: --chart-color-1, --chart-axis-color, --chart-tooltip-bg
```

**forms:**
```markdown
## Styling & Theming
Uses design-tokens for button, input, select styling.

Tokens: --button-bg-primary, --input-border-color, --input-padding-inline
```

**tables (future):**
```markdown
## Styling & Theming
Uses design-tokens for table borders, row colors, header styling.

Tokens: --table-border-color, --table-row-hover-bg, --table-header-bg
```

---

## Token Flow Diagram

```
User: "Create a dashboard with charts and forms"

Claude loads:
├─ design-tokens SKILL.md (5,000 tokens)
│   └─ Defines all styling tokens
│
├─ data-viz SKILL.md (5,000 tokens)
│   └─ References design-tokens for --chart-color-*
│       └─ design-tokens already loaded: 0 additional tokens
│
└─ forms SKILL.md (5,000 tokens)
    └─ References design-tokens for --button-bg-*, --input-border-*
        └─ design-tokens already loaded: 0 additional tokens

TOTAL: 15,000 tokens
WITHOUT HUB: 75,000+ tokens (theming repeated in each)
SAVINGS: 80%
```

---

## Benefits

### 1. **Single Source of Truth**
- Theme switching defined once in design-tokens
- All components inherit theme support
- Consistent behavior across skills

### 2. **Token Efficiency**
- Hub loaded once
- Spokes reference it (0 additional tokens)
- Scales to unlimited spokes

### 3. **Consistency**
- All components use same token naming
- Same theme switching mechanism
- Same accessibility patterns

### 4. **Maintainability**
- Update hub → all spokes benefit
- Add new theme → all components support it
- Fix bug once → affects all spokes

---

## Efficiency at Scale

**2 spokes:**
- Hub + 2 spokes: 15,000 tokens
- Without hub: 50,000 tokens
- **Savings: 70%**

**5 spokes:**
- Hub + 5 spokes: 30,000 tokens
- Without hub: 150,000 tokens
- **Savings: 80%**

**10 spokes:**
- Hub + 10 spokes: 55,000 tokens
- Without hub: 300,000 tokens
- **Savings: 82%**

**14 spokes (all component skills):**
- Hub + 14 spokes: 75,000 tokens
- Without hub: 500,000+ tokens
- **Savings: 85%** 🚀

---

## When to Use Hub-and-Spoke

**Use when:**
- ✅ Shared functionality needed across many skills
- ✅ Foundation skill that all components need
- ✅ Want to maximize token efficiency
- ✅ Consistency is critical

**Examples:**
- design-tokens (styling hub for all components)
- i18n (translation hub for all text)
- accessibility (a11y patterns hub)
- error-handling (error pattern hub)

**Don't use when:**
- Skills are truly independent (no shared needs)
- One-off integration (not reusable pattern)

---

## Design Principles

### 1. **Hub Should Be Foundational**
- Provides core functionality all spokes need
- Doesn't depend on spokes (one-way dependency)
- Rarely changes (stable interface)

### 2. **Spokes Reference Hub Explicitly**
- Document hub dependency in SKILL.md
- Show token/pattern usage
- Explain integration points

### 3. **Hub Documentation Shows Spoke Integration**
- design-tokens/SKILL.md includes "Component Integration" section
- Shows how spokes should consume hub
- Provides integration checklist

---

## Our Implementation

**Hub:** `design-tokens`
- Provides: Complete styling system
- Size: 5,000 tokens (SKILL.md)
- References: 5 detailed guides (loaded as needed)

**Current Spokes:**
- ✅ `data-viz` - Chart styling
- ✅ `forms` - Button/input styling

**Future Spokes (when complete):**
- 🚧 `tables` - Table styling
- 🚧 `dashboards` - Layout styling
- 🚧 `ai-chat` - Chat UI styling
- 🚧 `navigation` - Nav styling
- 🚧 `feedback` - Toast/alert styling
- 🚧 All 12 remaining skills

**Total potential spokes:** 14

**Token efficiency at full scale:**
- design-tokens + 14 skills: ~75,000 tokens
- Without hub: 500,000+ tokens
- **Savings: 85%** for entire library!

---

## Comparison with Other Patterns

| Pattern | Token Cost | Complexity | Use Case |
|---------|-----------|------------|----------|
| **Hub-and-Spoke** | Lowest | Low | Shared foundation (design-tokens) |
| **Linear Chain** | Medium | Medium | Sequential workflow (A → B → C) |
| **Parallel Composition** | Highest | High | Independent skills (A + B + C) |

**Hub-and-spoke is most efficient** for foundational skills like design-tokens.

---

**Status:** ✅ Implemented (design-tokens is the hub)
**Efficiency:** 70-85% token savings
**Scalability:** Unlimited spokes
**Current Spokes:** 2 (data-viz, forms)
**Future Spokes:** 12 more component skills
