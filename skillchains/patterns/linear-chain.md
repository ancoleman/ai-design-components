# Linear Chain Pattern

**Sequential skill dependencies (A → B → C)**

---

## Pattern Structure

```
Skill A → Skill B → Skill C
  ↓         ↓         ↓
Base    Builds on  Final
        Skill A   Output
```

**Characteristics:**
- Sequential dependency flow
- Each skill builds on previous
- Clear hierarchy of responsibility
- Moderate token efficiency

---

## Example: Data Processing Pipeline

### Future Chain (When Complete)

```
data-viz → tables → dashboards
   ↓         ↓          ↓
Charts   Data Grid   Layout
```

**Flow:**
1. **data-viz** provides chart components
2. **tables** provides data grid (may embed charts from data-viz)
3. **dashboards** provides layout (arranges tables + charts)

**Each skill references the previous one**

---

## Token Flow

```
User: "Create a dashboard with data tables and embedded charts"

Claude loads skills sequentially:

1. dashboards SKILL.md (5,000 tokens)
   ├─ Sees: "Use tables for data grids"
   └─ Triggers: tables skill

2. tables SKILL.md (5,000 tokens)
   ├─ Sees: "Use data-viz for inline charts"
   └─ Triggers: data-viz skill

3. data-viz SKILL.md (5,000 tokens)
   └─ Chart implementation

TOTAL: 15,000 tokens
```

**Progressive loading:** Each skill loads only when referenced by previous

---

## Real-World Example: Form Wizard

### Future Chain (When navigation Complete)

```
design-tokens → forms → navigation
      ↓           ↓          ↓
   Styling    Inputs    Multi-step
```

**Use case:** Multi-step signup form

**Flow:**
1. **design-tokens** provides button/input styling
2. **forms** provides form components and validation
3. **navigation** provides step-by-step wizard navigation

**Implementation:**
```tsx
// navigation provides wizard structure
<Wizard>
  <Step title="Account">
    {/* forms provides inputs */}
    <Input />  {/* Styled by design-tokens */}
  </Step>
  <Step title="Profile">
    <Input />
  </Step>
  <Step title="Confirm">
    <Button />  {/* Styled by design-tokens */}
  </Step>
</Wizard>
```

---

## Benefits

### 1. **Clear Dependency Order**
```
Base skill (design-tokens) must load first
↓
Mid-level skills (forms, data-viz) reference base
↓
High-level skills (dashboards) coordinate mid-level
```

### 2. **Progressive Loading**
- Load only what you need
- Start at highest level skill
- Load dependencies as needed

### 3. **Logical Hierarchy**
- Foundation → Components → Composition
- Easy to understand and maintain

---

## Efficiency Comparison

**2-skill linear chain:**
```
A → B
5k + 5k = 10k tokens
```

**3-skill linear chain:**
```
A → B → C
5k + 5k + 5k = 15k tokens
```

**4-skill linear chain:**
```
A → B → C → D
5k + 5k + 5k + 5k = 20k tokens
```

**Cost grows linearly** - still efficient vs. inline knowledge

---

## When to Use Linear Chains

**Use when:**
- ✅ Clear hierarchical dependency
- ✅ Each skill builds on previous
- ✅ Sequential workflow
- ✅ Skills form a pipeline

**Examples:**
- design-tokens → forms → navigation (styled multi-step forms)
- search-filter → tables → data-viz (search → display → visualize)
- forms → validation → feedback (input → validate → notify)

**Don't use when:**
- Skills are independent (use parallel composition)
- All skills need same foundation (use hub-and-spoke)

---

**Best for:** Sequential workflows with clear dependencies
**Efficiency:** Good (linear growth)
**Complexity:** Medium
