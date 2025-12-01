# Accessibility for Drag-and-Drop

## Table of Contents
- [Core Principles](#core-principles)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Alternative UI Patterns](#alternative-ui-patterns)
- [ARIA Patterns](#aria-patterns)
- [Testing Guidelines](#testing-guidelines)

## Core Principles

### The Accessibility Challenge

Drag-and-drop is inherently visual and mouse-centric, creating barriers for:
- Keyboard-only users
- Screen reader users
- Users with motor disabilities
- Touch device users with assistive tech

### Universal Design Approach

**Always provide:**
1. Full keyboard navigation
2. Clear announcements for screen readers
3. Alternative UI methods (buttons, forms)
4. Visual feedback for all states
5. Sufficient time for interactions

## Keyboard Navigation

### Standard Key Mappings

```tsx
// Recommended keyboard scheme for dnd-kit
const keyboardCoordinates = {
  start: ['Space', 'Enter'],      // Pick up item
  cancel: ['Escape'],              // Cancel drag
  end: ['Space', 'Enter'],         // Drop item
  up: ['ArrowUp', 'w', 'W'],      // Move up
  down: ['ArrowDown', 's', 'S'],  // Move down
  left: ['ArrowLeft', 'a', 'A'],  // Move left
  right: ['ArrowRight', 'd', 'D'], // Move right
};
```

### Implementation with dnd-kit

```tsx
import { KeyboardSensor, useSensor } from '@dnd-kit/core';
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable';

function AccessibleDragDrop() {
  const keyboardSensor = useSensor(KeyboardSensor, {
    coordinateGetter: sortableKeyboardCoordinates,
  });

  return (
    <DndContext sensors={[keyboardSensor]}>
      {/* Draggable content */}
    </DndContext>
  );
}
```

### Custom Keyboard Navigation

```tsx
// Enhanced keyboard handler with visual feedback
function useKeyboardDragDrop(items, onReorder) {
  const [activeIndex, setActiveIndex] = useState(-1);
  const [isGrabbed, setIsGrabbed] = useState(false);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (!items.length) return;

    switch (e.key) {
      case 'Tab':
        // Allow normal tab navigation when not dragging
        if (!isGrabbed) return;
        e.preventDefault();
        break;

      case ' ':
      case 'Enter':
        e.preventDefault();
        if (activeIndex === -1) {
          setActiveIndex(0);
        } else if (!isGrabbed) {
          // Pick up item
          setIsGrabbed(true);
          announceToScreenReader(`Grabbed ${items[activeIndex].label}. Use arrow keys to move.`);
        } else {
          // Drop item
          setIsGrabbed(false);
          announceToScreenReader(`Dropped ${items[activeIndex].label} at position ${activeIndex + 1}.`);
        }
        break;

      case 'Escape':
        if (isGrabbed) {
          e.preventDefault();
          setIsGrabbed(false);
          announceToScreenReader('Drag cancelled.');
        }
        break;

      case 'ArrowUp':
      case 'ArrowDown':
        e.preventDefault();
        if (isGrabbed) {
          const newIndex = e.key === 'ArrowUp'
            ? Math.max(0, activeIndex - 1)
            : Math.min(items.length - 1, activeIndex + 1);

          if (newIndex !== activeIndex) {
            onReorder(arrayMove(items, activeIndex, newIndex));
            setActiveIndex(newIndex);
            announceToScreenReader(`Moved to position ${newIndex + 1} of ${items.length}.`);
          }
        } else {
          // Navigate without dragging
          const newIndex = e.key === 'ArrowUp'
            ? Math.max(0, activeIndex - 1)
            : Math.min(items.length - 1, activeIndex + 1);
          setActiveIndex(newIndex);
        }
        break;
    }
  };

  return { activeIndex, isGrabbed, handleKeyDown };
}
```

## Screen Reader Support

### Live Region Announcements

```tsx
// Announcement component for screen readers
function DragDropAnnouncements({ children }) {
  return (
    <>
      {children}
      {/* Live region for announcements */}
      <div
        id="dnd-announcements"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
        style={{
          position: 'absolute',
          left: '-10000px',
          width: '1px',
          height: '1px',
          overflow: 'hidden',
        }}
      />
    </>
  );
}

// Helper function to announce
function announceToScreenReader(message: string) {
  const element = document.getElementById('dnd-announcements');
  if (element) {
    element.textContent = message;
    // Clear after announcement
    setTimeout(() => {
      element.textContent = '';
    }, 1000);
  }
}
```

### dnd-kit Accessibility Features

```tsx
import { Announcements } from '@dnd-kit/core';

// Custom announcement messages
const announcements: Announcements = {
  onDragStart(id) {
    return `Picked up draggable item ${id}. Press arrow keys to move, space to drop, escape to cancel.`;
  },
  onDragOver(id, overId) {
    if (overId) {
      return `Draggable item ${id} is over droppable area ${overId}.`;
    }
    return `Draggable item ${id} is no longer over a droppable area.`;
  },
  onDragEnd(id, overId) {
    if (overId) {
      return `Draggable item ${id} was dropped over droppable area ${overId}.`;
    }
    return `Draggable item ${id} was dropped.`;
  },
  onDragCancel(id) {
    return `Dragging was cancelled. Draggable item ${id} was dropped.`;
  },
};

// Use in DndContext
<DndContext announcements={announcements}>
  {/* Content */}
</DndContext>
```

## Alternative UI Patterns

### Move Buttons Pattern

Provide explicit move buttons as an alternative to drag-and-drop.

```tsx
function AccessibleListItem({ item, index, onMove, totalItems }) {
  return (
    <div className="list-item" role="listitem">
      <div className="item-content">{item.content}</div>

      {/* Alternative controls */}
      <div className="item-controls" role="group" aria-label="Reorder controls">
        <button
          onClick={() => onMove(index, index - 1)}
          disabled={index === 0}
          aria-label={`Move ${item.label} up`}
          title="Move up"
        >
          ↑
        </button>

        <button
          onClick={() => onMove(index, index + 1)}
          disabled={index === totalItems - 1}
          aria-label={`Move ${item.label} down`}
          title="Move down"
        >
          ↓
        </button>

        <select
          aria-label={`Move ${item.label} to position`}
          value={index}
          onChange={(e) => onMove(index, parseInt(e.target.value))}
        >
          {Array.from({ length: totalItems }, (_, i) => (
            <option key={i} value={i}>
              Position {i + 1}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
```

### Context Menu Pattern

Right-click or long-press menu for reordering.

```tsx
function ContextMenuReorder({ item, onAction }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });

  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setMenuPosition({ x: e.clientX, y: e.clientY });
    setMenuOpen(true);
  };

  return (
    <>
      <div
        onContextMenu={handleContextMenu}
        role="button"
        tabIndex={0}
        aria-haspopup="true"
        aria-expanded={menuOpen}
      >
        {item.content}
      </div>

      {menuOpen && (
        <div
          className="context-menu"
          style={{ left: menuPosition.x, top: menuPosition.y }}
          role="menu"
        >
          <button role="menuitem" onClick={() => onAction('moveUp')}>
            Move Up
          </button>
          <button role="menuitem" onClick={() => onAction('moveDown')}>
            Move Down
          </button>
          <button role="menuitem" onClick={() => onAction('moveToTop')}>
            Move to Top
          </button>
          <button role="menuitem" onClick={() => onAction('moveToBottom')}>
            Move to Bottom
          </button>
        </div>
      )}
    </>
  );
}
```

## ARIA Patterns

### Essential ARIA Attributes

```tsx
// Draggable item
<div
  role="button"
  tabIndex={0}
  aria-roledescription="sortable"
  aria-describedby="drag-instructions"
  aria-grabbed={isDragging}
  aria-dropeffect={canDrop ? "move" : "none"}
  aria-label={`${item.label}, position ${index + 1} of ${total}`}
>
  {item.content}
</div>

// Drag instructions (hidden but available to screen readers)
<div id="drag-instructions" className="sr-only">
  Press space or enter to start dragging.
  Use arrow keys to move the item.
  Press space or enter again to drop.
  Press escape to cancel.
</div>
```

### Drop Zone ARIA

```tsx
function DropZone({ isActive, canDrop, children }) {
  return (
    <div
      role="region"
      aria-dropeffect={canDrop ? "move" : "none"}
      aria-busy={isActive}
      aria-label="Drop zone"
      aria-describedby={isActive ? "drop-active" : "drop-inactive"}
    >
      {children}
      <span id="drop-active" className="sr-only">
        Drop zone active. Release to drop here.
      </span>
      <span id="drop-inactive" className="sr-only">
        Drop zone available.
      </span>
    </div>
  );
}
```

### List Reordering Pattern

```tsx
// Accessible sortable list
<div
  role="list"
  aria-label="Sortable task list"
  aria-describedby="list-instructions"
>
  {items.map((item, index) => (
    <div
      key={item.id}
      role="listitem"
      aria-setsize={items.length}
      aria-posinset={index + 1}
      tabIndex={activeIndex === index ? 0 : -1}
    >
      {/* Item content */}
    </div>
  ))}
</div>

<div id="list-instructions" className="sr-only">
  This is a reorderable list.
  Press Tab to focus an item, then press Space to grab it.
  Use arrow keys to move the item.
  Press Space again to drop it.
</div>
```

## Testing Guidelines

### Manual Testing Checklist

```markdown
## Keyboard Navigation
- [ ] Can reach all draggable items with Tab key
- [ ] Can initiate drag with Space/Enter
- [ ] Can move items with arrow keys
- [ ] Can cancel drag with Escape
- [ ] Can drop items with Space/Enter
- [ ] Focus visible at all times
- [ ] No keyboard traps

## Screen Reader Testing
- [ ] All items have descriptive labels
- [ ] Drag start announced
- [ ] Movement announced with position
- [ ] Drop location announced
- [ ] Instructions available
- [ ] Live region updates work

## Alternative UI
- [ ] Move buttons functional
- [ ] Position selector works
- [ ] Context menu accessible
- [ ] All alternatives keyboard accessible
```

### Automated Testing

```tsx
// Jest + Testing Library example
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('drag and drop is keyboard accessible', async () => {
  const user = userEvent.setup();
  render(<SortableList items={items} />);

  // Focus first item
  const firstItem = screen.getByRole('button', { name: /item 1/i });
  await user.tab();
  expect(firstItem).toHaveFocus();

  // Start drag
  await user.keyboard(' ');
  expect(firstItem).toHaveAttribute('aria-grabbed', 'true');

  // Move down
  await user.keyboard('{ArrowDown}');

  // Drop
  await user.keyboard(' ');
  expect(firstItem).toHaveAttribute('aria-grabbed', 'false');

  // Verify announcement
  expect(screen.getByRole('status')).toHaveTextContent(/dropped/i);
});
```

### Screen Reader Testing Tools

**Windows:**
- NVDA (free, recommended for testing)
- JAWS (commercial, widely used)

**macOS:**
- VoiceOver (built-in, Cmd+F5)

**Linux:**
- Orca (free, GNOME)

**Browser Extensions:**
- ChromeVox (Chrome)
- Screen Reader Simulator

### Testing Script

```bash
#!/bin/bash
# accessibility-test.sh

echo "🔍 Testing Drag-and-Drop Accessibility"

# Run automated tests
npm test -- --coverage drag-drop.test

# Check ARIA attributes
echo "Checking ARIA attributes..."
grep -r "aria-" ./src/components/drag-drop/

# Validate keyboard handlers
echo "Checking keyboard support..."
grep -r "onKeyDown\|handleKey" ./src/components/drag-drop/

# Check for alternative UI
echo "Checking alternative UI..."
grep -r "button.*move\|Move.*button" ./src/components/drag-drop/

echo "✅ Accessibility check complete"
```

## Best Practices Summary

### Do's
- ✅ Provide full keyboard navigation
- ✅ Include clear screen reader announcements
- ✅ Offer alternative UI methods
- ✅ Test with actual assistive technology
- ✅ Document keyboard shortcuts
- ✅ Use semantic HTML and ARIA correctly

### Don'ts
- ❌ Rely solely on drag-and-drop
- ❌ Hide important functionality behind drag
- ❌ Forget escape key handling
- ❌ Ignore focus management
- ❌ Skip screen reader testing
- ❌ Use placeholder text as labels

### Quick Implementation Checklist

```tsx
// Minimum viable accessible drag-and-drop
const AccessibleDragDrop = () => {
  // ✅ 1. Keyboard sensor
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor)
  );

  // ✅ 2. Announcements
  const announcements = {
    onDragStart: (id) => `Picked up ${id}`,
    onDragEnd: (id, overId) => `Dropped ${id} at ${overId}`,
  };

  // ✅ 3. ARIA attributes
  const ariaAttributes = {
    role: 'button',
    tabIndex: 0,
    'aria-roledescription': 'sortable',
    'aria-grabbed': isDragging,
  };

  // ✅ 4. Alternative UI
  const alternativeControls = (
    <button onClick={handleMoveWithoutDrag}>
      Move without dragging
    </button>
  );

  // ✅ 5. Instructions
  const instructions = (
    <div className="sr-only">
      Press space to grab, arrows to move, space to drop
    </div>
  );

  return (
    <DndContext sensors={sensors} announcements={announcements}>
      {instructions}
      {/* Draggable content with ARIA */}
      {alternativeControls}
    </DndContext>
  );
};
```