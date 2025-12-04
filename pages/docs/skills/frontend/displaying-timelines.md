---
sidebar_position: 12
title: Displaying Timelines
description: Chronological events and activity through timelines, feeds, Gantt charts, and calendars
tags: [frontend, timelines, activity-feeds, gantt, calendar]
---

# Displaying Timelines & Activity Components

Systematic creation of timeline and activity components, from simple vertical timelines to complex interactive Gantt charts.

## When to Use

Use this skill when:
- Creating activity feeds (social, notifications, audit logs)
- Displaying timelines (vertical, horizontal, interactive)
- Building Gantt charts or project schedules
- Implementing calendar interfaces (month, week, day views)
- Showing chronological events or historical data
- Handling real-time activity updates
- Requiring timestamp formatting (relative, absolute)
- Ensuring timeline accessibility or responsive behavior

## Quick Decision Framework

Select component type based on use case:

```
Social Activity        → Activity Feed (infinite scroll, reactions)
System Events          → Audit Log (searchable, exportable, precise timestamps)
User Notifications     → Notification Feed (read/unread, grouped by date)
Historical Events      → Vertical Timeline (milestones, alternating sides)
Project Planning       → Gantt Chart (dependencies, drag-to-reschedule)
Scheduling             → Calendar Interface (month/week/day views)
Interactive Roadmap    → Horizontal Timeline (zoom, pan, filter)
```

## Core Implementation Patterns

### Activity Feeds

**Social Feed Pattern:**
- User avatar + name + action description
- Relative timestamps ("2 hours ago")
- Reactions and comments
- Infinite scroll with pagination
- Real-time updates via WebSocket

**Notification Feed Pattern:**
- Grouped by date sections
- Read/unread states with indicators
- Mark all as read functionality
- Filter by notification type

**Audit Log Pattern:**
- System events with precise timestamps
- User action tracking
- Searchable with advanced filters
- Exportable (CSV, JSON)

### Timeline Visualizations

**Vertical Timeline:**
- Events stacked chronologically
- Connecting line with marker dots
- Date markers and event cards
- Optional alternating sides
- Best for: Historical events, project milestones

**Horizontal Timeline:**
- Events along horizontal axis
- Scroll or zoom to navigate
- Density varies by zoom level
- Best for: Project timelines, roadmaps

**Interactive Timeline:**
- Click events for detail view
- Filter by category/type
- Zoom in/out controls
- Pan and scroll navigation

### Gantt Charts

**Project Planning Features:**
- Tasks as horizontal bars
- Dependencies with arrows
- Critical path highlighting
- Drag to reschedule
- Progress indicators
- Milestone markers (diamonds)
- Zoom levels (day/week/month/year)

### Calendar Interfaces

**Month View:**
- Traditional calendar grid
- Events in date cells
- Click to create/edit
- Color-coded categories

**Week View:**
- Time slots (hourly)
- Events as draggable blocks
- Resize to change duration

**Day/Agenda View:**
- Detailed daily schedule
- List format with time duration
- Scrollable timeline

## Timestamp Formatting

Essential timestamp patterns:

**Relative (Recent Events):**
- "Just now" (&lt;1 min)
- "5 minutes ago"
- "3 hours ago"
- "Yesterday at 3:42 PM"

**Absolute (Older Events):**
- "Jan 15, 2025"
- "January 15, 2025 at 3:42 PM"
- ISO 8601 for APIs

**Implementation Considerations:**
- Timezone handling (display user's local time)
- Locale-aware formatting
- Hover for precise timestamp
- Auto-update relative times

## Real-Time Updates

**Live Activity Feed:**
- WebSocket or SSE for new events
- Smooth insertion animation
- "X new items" notification banner
- Click to load new items
- Optimistic updates for user actions

## Performance Optimization

Critical performance thresholds:

```
&lt;100 events       → Client-side rendering, no virtualization
100-1,000 events  → Virtual scrolling recommended
1,000+ events     → Virtual scrolling + server pagination
Real-time         → Debounce updates, batch insertions
```

## Library Recommendations

### Timeline: react-chrono (Flexible)

Best for timeline visualizations with rich content:
- Horizontal, vertical, alternating layouts
- Image and video support
- Custom item rendering
- TypeScript support
- Responsive out of the box

```bash
npm install react-chrono
```

### Gantt Charts: SVAR React Gantt

Best for project management:
- Modern, dependency-free
- Drag-and-drop tasks
- Dependencies and milestones
- Customizable appearance

```bash
npm install @svar/gantt
```

### Calendar: react-big-calendar

Best for scheduling interfaces:
- Month, week, day, agenda views
- Drag-and-drop events
- Customizable styling
- Large community support

```bash
npm install react-big-calendar
```

## Accessibility Requirements

Essential WCAG compliance:

**Semantic HTML:**
- Use `&lt;ol>` or `&lt;ul>` for timelines
- Proper heading hierarchy
- Semantic time elements

**ARIA Patterns:**
- `role="feed"` for activity feeds
- `role="article"` for timeline items
- `aria-label` for timestamps
- `aria-busy` during loading

**Keyboard Navigation:**
- Tab through interactive items
- Arrow keys for timeline navigation
- Enter/Space to expand items
- Skip to latest/oldest controls

## Design Token Integration

Timelines use the design-tokens skill for consistent theming:

**Timeline-Specific Tokens:**
- `--timeline-line-color` - Connecting line color
- `--timeline-dot-color` - Event marker color
- `--timeline-dot-active-color` - Current/active event
- `--event-card-bg` - Event card background

Supports light, dark, high-contrast, and custom themes.

## Related Skills

- [Theming Components](./theming-components.md) - Timeline styling
- [Providing Feedback](./providing-feedback.md) - Loading states for timelines
- [Visualizing Data](./visualizing-data.md) - Timeline data visualization
- [Creating Dashboards](./creating-dashboards.md) - Activity feed widgets

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/displaying-timelines)
- Patterns: `references/activity-feeds.md`, `references/vertical-timelines.md`, `references/gantt-patterns.md`
- Features: `references/real-time-updates.md`, `references/timestamp-formatting.md`
- Performance: `references/performance-optimization.md`
- Examples: `examples/social-activity-feed.tsx`, `examples/project-gantt.tsx`
