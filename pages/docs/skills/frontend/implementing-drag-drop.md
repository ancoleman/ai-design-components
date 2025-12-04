---
sidebar_position: 8
title: Implementing Drag Drop
description: Drag-and-drop and sortable interfaces with accessibility and touch support
tags: [frontend, drag-drop, kanban, sortable, accessibility]
---

# Implementing Drag-and-Drop & Sortable Interfaces

Implement drag-and-drop interactions and sortable interfaces using modern React/TypeScript libraries with accessibility-first approaches.

## When to Use

Use this skill when:
- Building Trello-style kanban boards with draggable cards
- Creating sortable lists with drag handles for priority ordering
- Implementing file upload zones with drag-and-drop feedback
- Building reorderable grids for dashboard widgets or galleries
- Creating visual builders with node-based interfaces
- Implementing any UI requiring spatial reorganization

## Overview

This skill helps implement drag-and-drop interactions and sortable interfaces using modern React/TypeScript libraries. It covers accessibility-first approaches, touch support, and performance optimization for creating intuitive direct manipulation UIs.

## Core Patterns

### Sortable Lists
- Vertical lists with drag handles
- Horizontal lists for tab/carousel reordering
- Grid layouts with 2D dragging
- Auto-scrolling near edges

### Kanban Boards
- Multi-column boards with cards
- WIP limits and swimlanes
- Card preview on hover
- Column management (add/remove/collapse)

### File Upload Zones
- Visual feedback states
- File type validation
- Multi-file handling
- Progress indicators

## Library Selection

### Primary: dnd-kit
Modern, accessible, and performant drag-and-drop for React.

**Key Features:**
- Built-in accessibility support
- Touch, mouse, and keyboard input
- Zero dependencies (~10KB core)
- Highly customizable
- TypeScript native

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

## Implementation Workflow

### Step 1: Analyze Requirements
Determine the drag-and-drop pattern needed:
- Simple list reordering → Sortable list pattern
- Multi-container movement → Kanban pattern
- File handling → Dropzone pattern
- Complex interactions → Visual builder pattern

### Step 2: Set Up Library
```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

### Step 3: Implement Core Functionality
Use examples as starting points:
- `examples/sortable-list.tsx` for basic lists
- `examples/kanban-board.tsx` for multi-column boards
- `examples/file-dropzone.tsx` for file uploads
- `examples/grid-reorder.tsx` for grid layouts

### Step 4: Add Accessibility
- Implement keyboard navigation
- Add screen reader announcements
- Provide alternative controls
- Test with assistive technologies

### Step 5: Optimize Performance
For lists with >100 items:
- Implement virtual scrolling
- Use efficient drop position calculations

## Mobile & Touch Support

Essential patterns:
- Long press to initiate drag
- Preventing scroll during drag
- Touch-friendly hit areas (44px minimum)
- Gesture conflict resolution

## State Management

Key considerations:
- Managing drag state in React
- Optimistic updates
- Undo/redo functionality
- Persisting order changes

## Best Practices

### Visual Feedback
- Show drag handles (⋮⋮) to indicate draggability
- Change cursor (grab → grabbing)
- Display drop zone placeholders
- Make dragged items semi-transparent
- Highlight valid drop targets

### Performance
- Use CSS transforms, not position properties
- Apply `will-change: transform` for animations
- Throttle drag events for large lists
- Implement virtual scrolling when needed

### Accessibility First
- Always provide keyboard alternatives
- Include screen reader announcements
- Test with NVDA/JAWS/VoiceOver
- Provide non-drag alternatives (buttons/forms)

### Error Handling
- Show invalid drop feedback
- Implement undo functionality
- Auto-save after successful drops
- Handle network failures gracefully

## Testing Checklist

Before deployment, verify:
- [ ] Keyboard navigation works completely
- [ ] Screen readers announce all actions
- [ ] Touch devices can drag smoothly
- [ ] Performance acceptable with expected data volume
- [ ] Visual feedback clear and responsive
- [ ] Undo/redo functionality works
- [ ] Alternative UI provided for accessibility
- [ ] Works across all target browsers

## Related Skills

- [Theming Components](./theming-components.md) - Drag state styling
- [Creating Dashboards](./creating-dashboards.md) - Reorderable dashboard widgets
- [Designing Layouts](./designing-layouts.md) - Grid layouts for draggable items
- [Providing Feedback](./providing-feedback.md) - Drag feedback states

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-drag-drop)
- Patterns: `references/dnd-patterns.md`, `references/kanban-implementation.md`
- Accessibility: `references/accessibility-dnd.md`
- Performance: `references/performance-optimization.md`
- Mobile: `references/touch-support.md`
- Examples: `examples/sortable-list.tsx`, `examples/kanban-board.tsx`
