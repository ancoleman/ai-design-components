# Skill Keyword Triggers

**Quick reference for which words/phrases trigger which skills.**

---

## Trigger Matrix

### theming-components (ALWAYS FIRST for visual work)

**Trigger words:**
- theme, theming, themed
- colors, color palette, brand colors
- dark mode, light mode, high contrast
- styling, styles, CSS variables
- design tokens, tokens
- typography, fonts
- spacing, layout spacing

**Example prompts:**
- "Set up theming for my app"
- "I need dark mode support"
- "Use my brand color #FF6B35"
- "Create a design system"

---

### designing-layouts

**Trigger words:**
- layout, layouts
- grid, columns, rows
- responsive, breakpoints, mobile
- sidebar, header, footer
- structure, page structure
- container, wrapper
- flexbox, CSS grid

**Example prompts:**
- "Create a 3-column layout"
- "I need a responsive dashboard grid"
- "Add a sidebar navigation layout"
- "Structure my page with header and main content"

---

### visualizing-data

**Trigger words:**
- chart, charts, graph, graphs
- visualization, visualize, visualizing
- plot, plotting
- bar chart, line chart, pie chart
- metrics, KPIs, analytics
- trends, comparisons
- data viz, dataviz

**Example prompts:**
- "Create a bar chart for sales data"
- "Visualize monthly revenue trends"
- "I need a pie chart showing market share"
- "Build analytics charts for my dashboard"

---

### building-tables

**Trigger words:**
- table, tables, data table
- grid, data grid
- rows, columns (data context)
- records, entries
- sortable, pagination
- spreadsheet-like

**Example prompts:**
- "Create a sortable data table"
- "I need a table showing customer records"
- "Build a paginated grid of products"
- "Display transaction history in a table"

---

### building-forms

**Trigger words:**
- form, forms
- input, inputs, fields
- login, signup, register, registration
- validation, validate
- submit, submission
- checkbox, radio, dropdown, select
- date picker, file upload

**Example prompts:**
- "Create a login form"
- "Build a multi-step registration form"
- "I need a contact form with validation"
- "Add filter inputs to my dashboard"

---

### providing-feedback

**Trigger words:**
- notification, notifications
- toast, toasts
- alert, alerts
- loading, spinner, skeleton
- progress, progress bar
- error message, success message
- feedback, user feedback

**Example prompts:**
- "Add toast notifications"
- "Show loading state while fetching"
- "Display error messages inline"
- "Create a progress indicator"

---

### implementing-navigation

**Trigger words:**
- navigation, nav, navbar
- menu, menus
- tabs, tab bar
- breadcrumbs
- routing, routes
- links, navigation links
- sidebar nav, top nav

**Example prompts:**
- "Create a navigation menu"
- "Build tabbed navigation"
- "Add breadcrumbs to my pages"
- "Set up routing for my app"

---

### implementing-search-filter

**Trigger words:**
- search, search bar
- filter, filters, filtering
- faceted, facets
- query, search query
- autocomplete, typeahead
- find, lookup

**Example prompts:**
- "Add a search bar"
- "Create filter controls for the table"
- "Build faceted search for products"
- "Implement autocomplete search"

---

### building-ai-chat

**Trigger words:**
- chat, chatbot, chat interface
- AI, AI assistant
- conversation, conversational
- messaging, messages
- streaming, stream response
- LLM, language model
- copilot, assistant

**Example prompts:**
- "Build an AI chat interface"
- "Create a chatbot UI"
- "Add a conversational assistant"
- "Implement streaming chat responses"

---

### managing-media

**Trigger words:**
- upload, file upload
- image, images, gallery
- video, audio, media
- files, file management
- drag and drop files
- preview, thumbnail

**Example prompts:**
- "Create a file uploader"
- "Build an image gallery"
- "Add video player component"
- "Implement drag-and-drop file upload"

---

### displaying-timelines

**Trigger words:**
- timeline, timelines
- activity, activity feed
- history, version history
- events, event log
- changelog, audit log
- chronological

**Example prompts:**
- "Create an activity timeline"
- "Show version history"
- "Build an event log display"
- "Display order status timeline"

---

### implementing-drag-drop

**Trigger words:**
- drag, drop, drag and drop
- sortable, reorderable
- kanban, kanban board
- reorder, rearrange
- move items

**Example prompts:**
- "Create a kanban board"
- "Make the list sortable"
- "Add drag-and-drop reordering"
- "Build a task board with lanes"

---

### guiding-users

**Trigger words:**
- onboarding, onboard
- tutorial, walkthrough
- guide, guided tour
- tooltip, tooltips
- help, help system
- first-time, new user
- tour, product tour

**Example prompts:**
- "Create an onboarding flow"
- "Add tooltips explaining features"
- "Build a product tour"
- "Guide new users through setup"

---

### creating-dashboards

**Trigger words:**
- dashboard, dashboards
- admin panel, admin
- analytics dashboard
- metrics dashboard
- KPI dashboard
- control panel
- overview, summary view

**Example prompts:**
- "Build an analytics dashboard"
- "Create an admin panel"
- "I need a metrics dashboard"
- "Design a sales overview dashboard"

---

## Compound Triggers (Multiple Skills)

When these combinations appear, invoke multiple skills:

| User Says | Skills to Chain |
|-----------|-----------------|
| "dashboard with charts and filters" | theming → layouts → visualizing-data → forms |
| "data table with search" | theming → tables → search-filter |
| "form with validation and notifications" | theming → forms → feedback |
| "sortable kanban with drag-drop" | theming → drag-drop → feedback |
| "chat interface with file upload" | theming → ai-chat → media → forms |
| "onboarding wizard with steps" | theming → guiding-users → navigation → forms |
| "media gallery with timeline" | theming → media → timelines |

---

## Priority Order

When multiple skills could apply, use this priority:

1. **theming-components** - Always first (establishes design tokens)
2. **designing-layouts** - Second for any multi-component UI
3. **Content skills** (visualizing-data, tables, forms, ai-chat, media, timelines)
4. **Enhancement skills** (search-filter, drag-drop, navigation)
5. **guiding-users** - For onboarding overlays
6. **providing-feedback** - Last (notifications, loading states)

---

## Anti-Patterns

**Don't trigger skills for:**
- Generic coding questions
- Non-UI work (backend, database, etc.)
- Questions about the skills themselves (use documentation)

**Trigger words that are NOT skill triggers:**
- "explain", "how does", "what is" → Answer directly
- "debug", "fix", "error" → Debug without skill invocation
- "refactor", "optimize" → Code review without skill invocation

---

## Prompting the User

After invoking a skill, guide the user with specific questions:

**After theming-components:**
> "Design tokens ready. What's next - layout structure or content components?"

**After designing-layouts:**
> "Layout set. What content goes in it - charts, tables, forms, or all three?"

**After visualizing-data:**
> "Charts configured. Need a data table for details, or filter controls?"

**After building-tables:**
> "Table ready. Want to add search/filter controls?"

**After building-forms:**
> "Form built. Need toast notifications or loading states?"

**After providing-feedback:**
> "Feedback patterns added. Your component is complete!"
