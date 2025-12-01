# AI-Assisted Component Library: Drag-and-Drop & Sortable Interfaces
## Master Plan for Drag-and-Drop Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025

---

## Executive Summary

Drag-and-drop interfaces enable direct manipulation and spatial organization. This skill covers sortable lists, kanban boards, file uploads, visual builders, and accessibility considerations for drag interactions.

---

## Component Taxonomy

### Sortable Lists

**Vertical List**
- Drag items up/down
- Visual placeholder on hover
- Smooth animations
- Touch support (mobile)
- **Use:** Priority lists, todos

**Horizontal List**
- Drag items left/right
- Carousel reordering
- Tab reordering
- **Use:** Image galleries, steps

**Grid/Multi-Column**
- 2D dragging
- Auto-layout on drop
- Masonry support
- **Use:** Dashboard widgets, card layouts

---

### Kanban Boards

**Columns + Cards**
- Drag cards between columns
- Drag to reorder within column
- Scroll on drag near edges
- Card preview on hover
- **Example:** Trello, Jira boards

**Features:**
- Add/delete columns
- Collapse columns
- Card count badges
- WIP limits
- Swimlanes (horizontal grouping)

---

### File Upload Drag-Drop

**Drop Zone**
- Visual feedback on dragover
- Accept only specific types
- Show file count on hover
- Error for invalid files
- **Use:** File uploads, image galleries

**Pattern:**
```javascript
onDrop(e) {
  e.preventDefault();
  const files = e.dataTransfer.files;
  // Handle files
}
```

---

### Visual Builders

**Drag to Connect**
- Nodes + edges
- Connection points (ports)
- Line routing
- **Use:** Flowcharts, mind maps, workflows

**Drag to Arrange**
- Canvas positioning
- Snap to grid (optional)
- Alignment guides
- **Use:** Design tools, wireframes

---

## Implementation Libraries

**React:**
- **react-beautiful-dnd**: Popular, smooth animations
- **dnd-kit**: Modern, accessible, modular
- **react-dnd**: Flexible, complex use cases

**Framework-Agnostic:**
- **SortableJS**: Vanilla JS, widely used
- **Dragula**: Simple, lightweight

---

## Accessibility Challenges

**Problem:** Drag-and-drop is mouse/touch-centric

**Solutions:**

**1. Keyboard Alternative**
- Arrow keys to select item
- Ctrl+Arrow to move up/down
- Enter to pick up, Space to drop

**2. Screen Reader Announcements**
```html
<div role="button" aria-label="Move item up" tabindex="0">
  <!-- Draggable item -->
</div>
```

**3. Alternative UI**
- "Move up/down" buttons
- Dropdown: "Move to position X"
- Form-based reordering

**ARIA Pattern:**
- `aria-grabbed="true"` when dragging
- `aria-dropeffect="move"` on drop targets
- Live region announces moves

---

## UX Best Practices

**Visual Feedback:**
- Drag handle (:::: icon) to indicate draggable
- Cursor changes (grab → grabbing)
- Placeholder shows drop position
- Dragged item slightly transparent
- Drop zones highlighted

**Animations:**
- Smooth position transitions (200-300ms)
- Bounce effect on drop (subtle)
- Cards shift to make room

**Touch Support:**
- Long press to initiate drag (mobile)
- Prevent scroll during drag
- Larger hit areas (44px min)

**Error Handling:**
- Invalid drop target (red border, snap back)
- Undo last move (Ctrl+Z)
- Auto-save after drop

---

## Performance Considerations

**Large Lists (>100 items):**
- Virtual scrolling + drag-drop
- Limit rendered items
- Throttle drag events

**Heavy Animations:**
- Use CSS transforms (not top/left)
- `will-change: transform`
- `requestAnimationFrame` for smoothness

---

## Skill Structure

```yaml
---
name: drag-drop-sortable
description: Component library for drag-and-drop and sortable interfaces. Covers sortable lists (vertical, horizontal, grid), kanban boards (columns, cards, swimlanes), file upload drag-drop, visual builders (flowcharts, connections), implementation libraries (react-beautiful-dnd, dnd-kit, SortableJS), accessibility alternatives (keyboard, screen readers), and performance optimization for large lists.
---
```

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate library recommendations.

---

## Recommended Libraries & Tools

### **Primary: dnd-kit** (Modern, Accessible)

**Library:** `/clauderic/dnd-kit`
**Trust Score:** 9.3/10
**Code Snippets:** 9+ (core), 232+ (website)

**Why dnd-kit?**
- Modern, actively maintained
- Accessibility built-in (`@dnd-kit/accessibility`)
- Touch, mouse, keyboard support
- Lightweight (~10KB core, zero deps)
- Highly customizable

**Installation:**
```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

**Note:** react-beautiful-dnd is deprecated (archived August 2025)

**Alternatives:** react-dnd, Pragmatic drag and drop

---

## Styling & Theming

### Design Token Integration

All drag-and-drop components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--draggable-bg` - Draggable item background
- `--draggable-border` - Draggable item border
- `--dragging-bg` - Item being dragged background
- `--drop-zone-border` - Drop zone border
- `--drop-zone-bg` - Drop zone background
- `--drop-zone-border-active` - Drop zone border when hovering
- `--drop-zone-bg-active` - Drop zone background when hovering
- `--placeholder-bg` - Drop placeholder background
- `--drag-handle-color` - Drag handle icon color

**Spacing Tokens:**
- `--draggable-padding` - Draggable item padding
- `--draggable-gap` - Space between draggable items
- `--drop-zone-padding` - Drop zone padding

**Border & Radius:**
- `--draggable-border-radius` - Draggable item corners
- `--drop-zone-border-radius` - Drop zone corners
- `--drop-zone-border-width` - Drop zone border thickness

**Shadow Tokens:**
- `--draggable-shadow` - Item at rest shadow
- `--dragging-shadow` - Item being dragged shadow (elevated)

**Motion Tokens:**
- `--drag-transition-duration` - Item movement animation
- `--drop-transition-duration` - Drop animation

**Cursor Tokens:**
- `--cursor-grab` - Cursor when hoverable
- `--cursor-grabbing` - Cursor when dragging

### Component-Specific Tokens

```css
/* Draggable Items */
--draggable-bg: var(--color-white);
--draggable-border: var(--color-border);
--draggable-padding: var(--spacing-md);
--draggable-border-radius: var(--radius-md);
--draggable-shadow: var(--shadow-sm);
--draggable-gap: var(--spacing-sm);

/* Dragging State */
--dragging-bg: var(--color-gray-50);
--dragging-shadow: var(--shadow-xl);
--dragging-opacity: 0.5;
--cursor-grabbing: grabbing;

/* Drop Zones */
--drop-zone-border: 2px dashed var(--color-border);
--drop-zone-bg: var(--color-bg-secondary);
--drop-zone-border-active: 2px solid var(--color-primary);
--drop-zone-bg-active: var(--color-primary-50);
--drop-zone-padding: var(--spacing-lg);
--drop-zone-border-radius: var(--radius-lg);

/* Placeholder */
--placeholder-bg: var(--color-gray-100);
--placeholder-border: 2px dashed var(--color-gray-300);

/* Drag Handle */
--drag-handle-color: var(--color-text-tertiary);
--cursor-grab: grab;

/* Animations */
--drag-transition-duration: var(--duration-fast);
--drop-transition-duration: var(--duration-normal);
```

### Theme Support

- ✅ **Light Mode** - Clear drag indicators
- ✅ **Dark Mode** - Adjusted contrast for visibility
- ✅ **High Contrast** - Strong drop zone boundaries
- ✅ **Custom Brand Themes** - Brand-colored drop zones

### Accessibility via Tokens

- **High Contrast Mode**: Strong visual feedback for drag states
- **Focus Indicators**: Clear focus on keyboard-accessible alternatives
- **Reduced Motion**: Disable drag animations
- **Keyboard Alternatives**: Token-styled move buttons

---

**END OF MASTER PLAN**
