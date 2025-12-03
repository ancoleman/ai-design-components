# Skill Chain Quick Start

**Reference this when a user wants to build UI components.**

---

## Step 1: Identify the Goal

Parse user's request for these keywords:

| Keywords | Workflow | First Skill |
|----------|----------|-------------|
| dashboard, analytics, metrics, admin | Dashboard | theming-components |
| chart, graph, visualize, plot | Data Viz | theming-components |
| form, login, signup, input | Forms | theming-components |
| table, grid, records, list | Tables | theming-components |
| chat, AI, assistant | AI Chat | theming-components |

---

## Step 2: Announce the Chain

Tell the user what skills you'll invoke:

```
I'll guide you through these skills:
1. theming-components → [purpose]
2. [next skill] → [purpose]
3. [next skill] → [purpose]

Let's start with theming.
```

---

## Step 3: Invoke Skills in Order

**Always start with:**
```
Skill({ skill: "ui-data-skills:theming-components" })
```

**Then based on goal:**
- Dashboard: layouts → visualizing-data → building-tables → building-forms
- Charts: visualizing-data
- Forms: building-forms → providing-feedback
- Tables: building-tables → implementing-search-filter

---

## Step 4: Ask Questions from Each Skill

After invoking a skill, use its decision tree to ask the user:

**Theming:** "Brand color? Theme modes?"
**Layouts:** "Grid columns? Sidebar? Responsive?"
**Data Viz:** "Data type? Chart purpose? Volume?"
**Tables:** "Sortable? Pagination? Row count?"
**Forms:** "Input types? Validation? Multi-step?"

---

## Step 5: Apply Choices and Move to Next

After user answers:
1. Summarize what was configured
2. Announce next step
3. Invoke next skill
4. Repeat questions

---

## Step 6: Complete and Summarize

When all skills are invoked:
```
✅ Skill Chain Complete!

Summary:
- Theming: [what was set]
- Layout: [what was chosen]
- Components: [what was built]

All components use CSS variables from design tokens.
Theme switching works automatically.
```

---

## Quick Command Reference

**Invoke a skill:**
```
Skill({ skill: "ui-data-skills:[skill-name]" })
```

**Available skills:**
- theming-components
- designing-layouts
- visualizing-data
- building-tables
- building-forms
- providing-feedback
- implementing-navigation
- implementing-search-filter
- building-ai-chat
- managing-media
- displaying-timelines
- implementing-drag-drop
- guiding-users
- creating-dashboards

---

## Example Flow

```
User: "Build me a sales dashboard"

Claude: "I'll guide you through: theming → layouts → data-viz → forms"

[Invoke theming-components]
Claude: "Brand color? Theme support?"
User: "#3B82F6, dark mode"

[Invoke designing-layouts]
Claude: "Layout structure?"
User: "3-column grid"

[Invoke visualizing-data]
Claude: "What metrics? Chart type?"
User: "Revenue trends, line chart"

[Invoke building-forms]
Claude: "What filters?"
User: "Date range"

Claude: "✅ Complete! Generated themed dashboard with charts and filters."
```

---

**Full documentation:** See other files in this directory.
