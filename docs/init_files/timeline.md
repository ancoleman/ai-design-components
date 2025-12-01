# AI-Assisted Component Library: Timeline & Activity Components
## Master Plan for Timeline Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025

---

## Executive Summary

Timeline components display chronological events, activities, and progress. This skill covers activity feeds, timeline visualizations, Gantt charts, and calendar interfaces.

---

## Component Taxonomy

### Activity Feeds

**Social Feed**
- User avatar + name
- Action description
- Timestamp (relative: "2 hours ago")
- Reactions/comments
- Infinite scroll
- **Example:** Facebook, Twitter feeds

**Notification Feed**
- Grouped by date
- Read/unread states
- Mark all as read
- Action buttons
- Filter by type

**Audit Log**
- System events
- User actions
- Timestamps (precise)
- Searchable
- Exportable

---

### Timeline Visualizations

**Vertical Timeline**
- Events stacked vertically
- Connecting line
- Date markers
- Alternating sides (optional)
- **Best for:** Historical events, project milestones

**Horizontal Timeline**
- Events along horizontal axis
- Scroll or zoom to navigate
- Density varies by zoom level
- **Best for:** Project timelines, roadmaps

**Interactive Timeline**
- Click events for details
- Filter by category
- Zoom in/out
- Pan/scroll
- **Libraries:** vis-timeline, react-timeline

---

### Gantt Charts

**Project Planning**
- Tasks as horizontal bars
- Dependencies (arrows)
- Critical path highlighting
- Drag to reschedule
- Progress indicators

**Features:**
- Milestones (diamonds)
- Resource allocation
- Today marker
- Zoom (day/week/month/year)

---

### Calendar Interfaces

**Month View**
- Traditional calendar grid
- Events in cells
- Click to create/edit
- Color-coded categories

**Week View**
- Time slots (hourly)
- Events as blocks
- Drag to resize/move
- Multiple calendars overlay

**Day/Agenda View**
- Detailed daily schedule
- List format
- Time duration
- Location, attendees

---

## Timestamp Formatting

**Relative (Recent):**
- "Just now" (<1 min)
- "5 minutes ago"
- "3 hours ago"
- "Yesterday at 3:42 PM"

**Absolute (Older):**
- "Jan 15, 2025"
- "January 15, 2025 at 3:42 PM"
- ISO 8601 for APIs

**Considerations:**
- Timezone handling
- Locale-aware formatting
- Hover for precise timestamp

---

## Real-Time Updates

**Live Activity Feed:**
- WebSocket or SSE for new events
- Smooth insertion animation
- "X new items" notification
- Click to load new

**Optimistic Updates:**
- Show user action immediately
- Update timestamp to "Just now"
- Rollback if error

---

## Skill Structure

```yaml
---
name: timeline-activity
description: Component library for timeline and activity displays. Covers activity feeds (social, notifications, audit logs), timeline visualizations (vertical, horizontal, interactive), Gantt charts (project planning, dependencies, milestones), calendar interfaces (month, week, day views), timestamp formatting (relative, absolute), and real-time updates.
---
```

---

## Styling & Theming

### Design Token Integration

All timeline and activity components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--timeline-line-color` - Vertical/horizontal timeline line
- `--timeline-dot-color` - Event marker dots
- `--timeline-dot-active-color` - Active/current event
- `--event-card-bg` - Event card background
- `--event-card-border` - Event card border
- `--timestamp-color` - Timestamp text color
- `--activity-item-bg` - Activity feed item background
- `--activity-item-hover-bg` - Item hover state
- `--gantt-bar-color` - Gantt task bar
- `--gantt-dependency-color` - Dependency arrow color

**Spacing Tokens:**
- `--timeline-gap` - Space between timeline items
- `--timeline-dot-size` - Event marker size
- `--event-card-padding` - Event card padding
- `--activity-item-padding` - Activity item padding

**Typography Tokens:**
- `--timestamp-font-size` - Timestamp text size
- `--event-title-font-size` - Event title size
- `--event-title-font-weight` - Event title weight

**Border & Radius:**
- `--timeline-line-width` - Timeline line thickness
- `--event-card-border-radius` - Event card corners
- `--timeline-dot-border-width` - Event marker border

**Shadow Tokens:**
- `--event-card-shadow` - Event card elevation
- `--activity-item-shadow` - Activity item shadow

### Component-Specific Tokens

```css
/* Timeline */
--timeline-line-color: var(--color-border);
--timeline-line-width: 2px;
--timeline-dot-color: var(--color-primary);
--timeline-dot-size: 12px;
--timeline-dot-active-color: var(--color-primary-600);
--timeline-gap: var(--spacing-lg);

/* Event Cards */
--event-card-bg: var(--color-white);
--event-card-border: var(--color-border);
--event-card-padding: var(--spacing-md);
--event-card-border-radius: var(--radius-md);
--event-card-shadow: var(--shadow-sm);

/* Activity Feed */
--activity-item-bg: var(--color-white);
--activity-item-hover-bg: var(--color-gray-50);
--activity-item-padding: var(--spacing-md);

/* Timestamps */
--timestamp-color: var(--color-text-secondary);
--timestamp-font-size: var(--font-size-sm);

/* Gantt Charts */
--gantt-bar-color: var(--color-primary);
--gantt-bar-height: 24px;
--gantt-dependency-color: var(--color-text-tertiary);
--gantt-grid-color: var(--color-border);
```

### Theme Support

- ✅ **Light Mode** - Clear chronological presentation
- ✅ **Dark Mode** - Adjusted for dark interfaces
- ✅ **High Contrast** - Strong timeline line visibility
- ✅ **Custom Brand Themes** - Brand-colored event markers

### Accessibility via Tokens

- **High Contrast Mode**: Strong timeline line and marker visibility
- **Focus Indicators**: Clear focus on interactive timeline items
- **Reduced Motion**: Disable timeline animations
- **Screen Readers**: Token-styled semantic HTML

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate library recommendations.

---

## Recommended Libraries & Tools

### **Timeline: react-chrono** (Flexible)

**Features:** Horizontal, vertical, alternating layouts. Images, videos, custom items.

**Alternatives:**
- react-vertical-timeline (simple, clean)
- Custom with CSS + design tokens

**Gantt Charts:** Bryntum Gantt, Syncfusion, SVAR React Gantt

**Calendar:** react-big-calendar, FullCalendar, react-day-picker

---

**END OF MASTER PLAN**
