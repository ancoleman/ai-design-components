# Skill Chaining Demo

**Use the `/skillchain` command to build UI components through guided skill chaining.**

---

## Quick Start

```bash
/skillchain help
```

Shows all 14 available skills and usage examples.

```bash
/skillchain sales dashboard with revenue charts
```

Starts a guided workflow that invokes the right skills in the right order.

---

## The `/skillchain` Command

### Usage

```
/skillchain [your goal]
```

### Examples

| Command | Skills Invoked |
|---------|----------------|
| `/skillchain dashboard with charts` | theming → layouts → dashboards → data-viz → forms |
| `/skillchain login form with validation` | theming → forms → feedback |
| `/skillchain data table with search` | theming → tables → search-filter |
| `/skillchain AI chat interface` | theming → ai-chat → forms |
| `/skillchain file upload gallery` | theming → media |
| `/skillchain kanban board` | theming → drag-drop |
| `/skillchain onboarding wizard` | theming → guiding-users |

### Workflow Commands

During a skill chain session, you can say:

| Command | Action |
|---------|--------|
| `back` | Return to previous step |
| `skip` | Use defaults, move to next step |
| `status` | Show current progress |
| `done` | Finish early with current selections |
| `restart` | Start over from beginning |

---

## Available Skills (14)

### Foundation
- **theming-components** - Colors, tokens, dark mode, branding

### Data Display
- **visualizing-data** - Charts, graphs (24+ types)
- **building-tables** - Data grids, sorting, pagination
- **creating-dashboards** - Dashboard layouts, KPI cards

### User Input
- **building-forms** - Forms, validation (50+ input types)
- **implementing-search-filter** - Search bars, faceted filters

### Interaction
- **building-ai-chat** - Chat UI, streaming, AI interfaces
- **implementing-drag-drop** - Kanban, sortable lists
- **providing-feedback** - Toasts, alerts, loading states

### Structure
- **implementing-navigation** - Menus, tabs, breadcrumbs
- **designing-layouts** - Grids, responsive, sidebars
- **displaying-timelines** - Activity feeds, history

### Content
- **managing-media** - File upload, galleries, video/audio
- **guiding-users** - Onboarding, tutorials, tooltips

---

## How It Works

1. **You run `/skillchain [goal]`**
2. **Claude parses your keywords** to identify which skills are needed
3. **Claude announces the skill chain** (e.g., "theming → data-viz → forms")
4. **Claude invokes each skill** using the Skill tool
5. **After each skill loads**, Claude asks you configuration questions
6. **Your answers shape the output** - chart types, layouts, features
7. **All skills chain together** for consistent, themed components

### Skill Order

```
theming (always first)
    ↓
structure (layouts, navigation)
    ↓
content (charts, tables, forms, chat, media)
    ↓
enhancement (search, drag-drop)
    ↓
feedback (notifications, loading states)
```

### Token Efficiency

Skills are designed to chain efficiently:
- **theming** loads once, used by all other skills
- **70-85% token savings** vs inline styling in each skill
- **Consistent design** across all components

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `KEYWORD_TRIGGERS.md` | Which words trigger which skills |
| `DECISION_TREE.md` | Decision trees for skill and option selection |
| `USER_PROMPTS.md` | Exact prompts used at each workflow step |
| `QUICKSTART.md` | Quick reference for orchestrating chains |
| `SKILLCHAIN_WORKFLOW.md` | Complete workflow documentation |

---

## Example Session

```
> /skillchain sales dashboard with monthly revenue

🔗 Skill Chain Initiated

Goal: Sales dashboard with monthly revenue visualization

I'll guide you through these skills:
1. theming-components → Design foundation
2. designing-layouts → Dashboard grid
3. visualizing-data → Revenue charts
4. building-forms → Date filters

Starting with theming...

[Invokes: theming-components skill]

🎨 Theming Configuration

Before building components, let's set up your design tokens:

1. Brand Color: What's your primary color?
2. Theme Modes: A) Light only  B) Light + Dark  C) Light + Dark + High Contrast

Reply with: [color], [A/B/C]

> #3B82F6, B

✅ Theming configured: Blue primary, light + dark mode

[Invokes: designing-layouts skill]

📐 Layout Configuration

Choose your layout structure:
A) Header + grid of cards
B) Sidebar + main content
C) Full-width sections

> A

✅ Layout: 3-column responsive card grid

[Invokes: visualizing-data skill]

📊 Chart Configuration

For monthly revenue, I recommend:
- Line chart for trends
- Bar chart for month comparison

Which do you prefer?

> Both - line for trend, bar for comparison

✅ Charts: Line chart (trend) + Bar chart (comparison)

[Invokes: building-forms skill]

📝 Filter Configuration

What filters do you need?
- Date range picker
- Category dropdown
- Search

> Date range and category

✅ Skill Chain Complete!

Summary:
- Theming: #3B82F6, light + dark mode
- Layout: Header + 3-column grid, responsive
- Charts: Line (trends) + Bar (comparison)
- Filters: Date range + Category dropdown

Would you like me to generate the full code?
```

---

## Command Location

The `/skillchain` command is defined in:

```
.claude/commands/skillchain.md
```

It references these support files:
- `demo/KEYWORD_TRIGGERS.md`
- `demo/DECISION_TREE.md`
- `demo/USER_PROMPTS.md`
- `demo/QUICKSTART.md`
