# User Guidance Prompts

**Exact prompts Claude should use to guide users through each skill chain step.**

---

## Initial Goal Recognition

When user states a goal, Claude responds:

### Dashboard Goal Detected
```
I'll help you build that dashboard. Based on your request, I'll guide you through these skills:

📊 **Skill Chain: Dashboard Workflow**
1. theming-components → Establish colors and design tokens
2. designing-layouts → Set up dashboard grid structure
3. visualizing-data → Create your charts and graphs
4. building-tables → Add data tables (if needed)
5. building-forms → Add filter controls
6. providing-feedback → Add loading states and notifications

Let's start with **theming**.

---

**🎨 Step 1: Theming**

I need to know your preferences:

**Brand Color:**
- Do you have a specific brand color? (e.g., "#3B82F6")
- Or should I use the default blue palette?

**Theme Support:**
A) Light mode only
B) Light + Dark mode
C) Light + Dark + High Contrast (accessibility)

Reply with your color and theme choice (e.g., "#FF6B35, B")
```

---

### Chart Goal Detected
```
I'll help you create that visualization.

📈 **Skill Chain: Data Visualization**
1. theming-components → Set chart colors
2. visualizing-data → Build your chart

Let's start with **theming**.

---

**🎨 Step 1: Theming**

For charts, I need to know:

**Color Palette:**
A) Default IBM colorblind-safe palette (recommended)
B) Custom brand colors
C) Monochromatic (single color variations)

**Theme Support:**
A) Light mode only
B) Light + Dark mode

Reply with your choices (e.g., "A, B")
```

---

### Form Goal Detected
```
I'll help you build that form.

📝 **Skill Chain: Form Workflow**
1. theming-components → Style inputs and buttons
2. building-forms → Create form structure and validation
3. providing-feedback → Add success/error messages

Let's start with **theming**.

---

**🎨 Step 1: Theming**

For forms, I need:

**Primary Button Color:**
- Brand color for submit buttons (e.g., "#3B82F6")
- Or use default blue?

**Input Style:**
A) Outlined inputs (border visible)
B) Filled inputs (background color)
C) Underlined inputs (minimal)

Reply with your color and style (e.g., "#22C55E, A")
```

---

## Step Transition Prompts

### After theming-components → Next Step

**Going to layouts:**
```
✅ **Theming Complete**

Design tokens established:
- Primary color: [color]
- Theme support: [light/dark/high-contrast]
- Tokens: colors, spacing, typography, shadows

---

**📐 Step 2: Layout Structure**

Now let's define your dashboard layout.

**Layout Options:**
A) **Header + 3-column grid** - Classic dashboard with cards
B) **Sidebar + main content** - Navigation-focused layout
C) **Full-width stacked** - Vertical sections, mobile-friendly
D) **Complex** - Header, sidebar, and widget areas

**Responsive Behavior:**
- 3 columns on desktop → 2 on tablet → 1 on mobile? (Y/N)

Reply with layout choice and responsive preference (e.g., "A, Y")
```

**Going to data-viz (no layout needed):**
```
✅ **Theming Complete**

Design tokens established with your chart colors.

---

**📊 Step 2: Chart Selection**

Now let's build your visualization.

**What type of data are you showing?**
A) **Categorical** - Comparing categories (products, regions)
B) **Time series** - Trends over time (daily, monthly)
C) **Numerical** - Distribution or correlation of numbers
D) **Hierarchical** - Nested data (org chart, categories)

Reply with your data type (e.g., "B")
```

---

### After designing-layouts → visualizing-data

```
✅ **Layout Complete**

Dashboard structure:
- [Layout type description]
- Responsive: [Yes/No]
- Grid areas defined

---

**📊 Step 3: Data Visualization**

Now let's add your charts.

**What metrics are you displaying?**

Tell me about your data:
1. What are you measuring? (revenue, users, conversions, etc.)
2. Over what time period? (daily, monthly, quarterly)
3. Any comparisons? (this year vs last, by category)

Example: "Monthly revenue for the past 12 months, compared by product category"
```

---

### After visualizing-data → Chart Type Selection

```
Based on your data, here are my recommendations:

**Your data:** [user's description]

**Recommended Chart Types:**

For [specific metric]:
A) **Bar Chart** - Best for comparing [X] values side by side
B) **Line Chart** - Best for showing [X] trend over time
C) **Area Chart** - Best for emphasizing volume/magnitude

For [second metric if applicable]:
D) **Pie Chart** - Shows composition (max 6 slices)
E) **Stacked Bar** - Compare composition across categories

**Additional Options:**
F) **Multi-line Chart** - Multiple metrics on same chart
G) **Small Multiples** - Separate charts for each category

Which chart types do you want? (e.g., "A for revenue, F for trends")
```

---

### After chart selection → Tables or Forms

```
✅ **Charts Complete**

Created:
- [Chart 1 description]
- [Chart 2 description]
Using tokens: --chart-color-1 through --chart-color-5

---

**What's next?**

A) **Add a data table** - Show detailed records below charts
B) **Add filter controls** - Date range, category filters
C) **Both** - Table with filter controls
D) **Done** - Charts are sufficient

Reply with your choice (e.g., "C")
```

---

### building-tables Prompts

```
**📋 Data Table Configuration**

Tell me about your table data:

**Columns:**
What fields do you want to display?
Example: "Date, Product, Quantity, Revenue, Status"

**Features needed:**
A) Sortable columns
B) Pagination (how many rows per page?)
C) Row selection (checkboxes)
D) Inline actions (edit, delete buttons)
E) Export to CSV

**Data volume:**
Approximately how many rows? (<100, 100-1000, 1000+)

Reply with columns, features, and volume
Example: "Date, Product, Revenue, Status | A, B(25), E | 500 rows"
```

---

### building-forms Prompts (for filters)

```
**🔍 Filter Controls**

What filters do you need for your dashboard?

**Filter Options:**
A) **Date range** - Start and end date pickers
B) **Category dropdown** - Select one category
C) **Multi-select** - Select multiple categories
D) **Search box** - Text search
E) **Range slider** - Numeric range (e.g., price)

**Filter behavior:**
1) **Auto-apply** - Filter updates data immediately
2) **Apply button** - User clicks to apply filters

Reply with filters and behavior
Example: "A, B, D | 1"
```

---

### building-forms Prompts (for standalone form)

```
**📝 Form Builder**

What information are you collecting?

**Field 1:** [Type + Label]
Examples:
- "text: Full Name"
- "email: Email Address"
- "password: Password"
- "select: Country (list options)"
- "date: Birth Date"
- "checkbox: Accept Terms"

**Validation:**
- Required fields?
- Email format validation?
- Password strength requirements?
- Custom validation?

**Form Structure:**
A) Single page form
B) Multi-step wizard
C) Inline editing

List your fields, validation needs, and structure choice.
```

---

### providing-feedback Prompts

```
**💬 Feedback & Notifications**

Final step - how should the UI communicate with users?

**Loading States:**
A) Spinner overlay for full-page loads
B) Skeleton loaders for components
C) Button loading states
D) Progress bars for uploads

**Notifications:**
E) Toast messages (auto-dismiss)
F) Alert dialogs (require action)
G) Inline success/error messages

**Empty States:**
H) "No data" illustrations
I) "No results found" messages

Which do you need? (e.g., "B, E, G, I")
```

---

## Completion Prompt

```
✅ **Skill Chain Complete!**

**Summary of what was built:**

🎨 **Theming:**
- Primary color: [color]
- Themes: [light/dark/etc]
- Design tokens: CSS variables for all components

📐 **Layout:**
- [Layout description]
- Responsive: [Yes/No]

📊 **Visualizations:**
- [Chart 1]
- [Chart 2]

📋 **Data Table:** [if applicable]
- Columns: [list]
- Features: [list]

🔍 **Filters:** [if applicable]
- [Filter list]

💬 **Feedback:**
- [Loading/notification patterns]

---

**Generated Code:**

The components use CSS variables from your design tokens, so theme switching works automatically:

\`\`\`javascript
// Toggle between themes
document.documentElement.setAttribute('data-theme', 'dark');
\`\`\`

Would you like me to:
A) Generate the full component code
B) Explain how the skill chain works
C) Make modifications to any part
```

---

## Error/Clarification Prompts

### Unclear Goal
```
I want to help, but I need a bit more clarity.

**What are you trying to build?**
- Dashboard with charts and metrics?
- Form for collecting user data?
- Data table for displaying records?
- Something else?

**Quick examples:**
- "Build a sales dashboard with monthly revenue charts"
- "Create a login form with validation"
- "Make a data table showing customer orders"

Please describe your goal in a sentence or two.
```

### Missing Information
```
I need a bit more information to continue.

**For [current skill], please tell me:**
- [Specific question 1]
- [Specific question 2]

Or say "skip" to use defaults, or "back" to revisit the previous step.
```

### Invalid Choice
```
I didn't understand that choice.

**Please reply with one of these options:**
A) [Option A description]
B) [Option B description]
C) [Option C description]

Or describe what you want in your own words.
```

---

## Navigation Commands

Users can say these at any point:

| Command | Action |
|---------|--------|
| "back" | Go to previous step |
| "skip" | Use defaults for current step |
| "restart" | Start over from beginning |
| "status" | Show current progress |
| "help" | Explain current step |
| "done" | Finish early with current selections |
