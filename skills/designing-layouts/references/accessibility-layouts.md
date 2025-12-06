# Accessibility in Layouts


## Table of Contents

- [Semantic HTML Structure](#semantic-html-structure)
  - [Landmark Regions](#landmark-regions)
  - [Skip Links](#skip-links)
- [Focus Management](#focus-management)
  - [Focus Trap for Modals](#focus-trap-for-modals)
  - [Focus Restoration](#focus-restoration)
- [ARIA Attributes](#aria-attributes)
  - [Live Regions](#live-regions)
  - [Expanded/Collapsed States](#expandedcollapsed-states)
  - [Describedby and Labelledby](#describedby-and-labelledby)
- [Keyboard Navigation](#keyboard-navigation)
  - [Keyboard Patterns](#keyboard-patterns)
  - [Grid Navigation](#grid-navigation)
- [Responsive Accessibility](#responsive-accessibility)
  - [Touch Target Sizing](#touch-target-sizing)
  - [Focus Indicators](#focus-indicators)
- [Screen Reader Helpers](#screen-reader-helpers)
  - [Visually Hidden](#visually-hidden)
  - [Announcing Changes](#announcing-changes)
- [Testing Accessibility](#testing-accessibility)
  - [Accessibility Checklist](#accessibility-checklist)
  - [Testing Tools](#testing-tools)
- [Common Patterns](#common-patterns)
  - [Responsive Table](#responsive-table)

## Semantic HTML Structure

### Landmark Regions

Use semantic HTML5 elements to create accessible page structure.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accessible Layout</title>
</head>
<body>
  <!-- Skip Links -->
  <a href="#main" class="skip-link">Skip to main content</a>
  <a href="#nav" class="skip-link">Skip to navigation</a>

  <!-- Header Landmark -->
  <header role="banner">
    <h1>Site Title</h1>
    <!-- Site-wide header content -->
  </header>

  <!-- Navigation Landmark -->
  <nav id="nav" role="navigation" aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li aria-current="page"><a href="/contact">Contact</a></li>
    </ul>
  </nav>

  <!-- Main Content Landmark -->
  <main id="main" role="main">
    <article>
      <h2>Article Title</h2>
      <!-- Main content -->
    </article>

    <!-- Complementary Content -->
    <aside role="complementary" aria-label="Related information">
      <!-- Sidebar content -->
    </aside>
  </main>

  <!-- Footer Landmark -->
  <footer role="contentinfo">
    <!-- Site-wide footer content -->
  </footer>
</body>
</html>
```

### Skip Links

Essential for keyboard navigation to bypass repetitive content.

```css
/* Skip link styling */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary-color);
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
  border-radius: 0 0 4px 0;
}

.skip-link:focus {
  top: 0;
}

/* Ensure focus is visible */
:focus {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

/* Never remove focus indicators without providing alternative */
:focus:not(:focus-visible) {
  outline: 2px solid transparent;
}

:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

## Focus Management

### Focus Trap for Modals

```typescript
export function trapFocus(element: HTMLElement) {
  const focusableElements = element.querySelectorAll(
    'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );

  const firstFocusable = focusableElements[0] as HTMLElement;
  const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement;

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      }
    } else {
      // Tab
      if (document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
  }

  element.addEventListener('keydown', handleKeyDown);
  firstFocusable?.focus();

  return () => {
    element.removeEventListener('keydown', handleKeyDown);
  };
}
```

### Focus Restoration

```typescript
export function useFocusRestore() {
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    previousFocus.current = document.activeElement as HTMLElement;

    return () => {
      previousFocus.current?.focus();
    };
  }, []);

  return previousFocus;
}

// Usage in modal component
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useFocusRestore();

  useEffect(() => {
    if (isOpen && modalRef.current) {
      const cleanup = trapFocus(modalRef.current);
      return cleanup;
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      {children}
    </div>
  );
}
```

## ARIA Attributes

### Live Regions

```html
<!-- Announce changes to screen readers -->
<div aria-live="polite" aria-atomic="true">
  <p>Form saved successfully</p>
</div>

<!-- Urgent announcements -->
<div role="alert" aria-live="assertive">
  <p>Error: Invalid email address</p>
</div>

<!-- Status updates -->
<div role="status" aria-live="polite">
  <p>3 items in your cart</p>
</div>
```

### Expanded/Collapsed States

```tsx
function CollapsibleSection({ title, children }: CollapsibleProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const contentId = useId();

  return (
    <section>
      <button
        aria-expanded={isExpanded}
        aria-controls={contentId}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {title}
        <span aria-hidden="true">{isExpanded ? '▼' : '▶'}</span>
      </button>

      <div
        id={contentId}
        hidden={!isExpanded}
        aria-hidden={!isExpanded}
      >
        {children}
      </div>
    </section>
  );
}
```

### Describedby and Labelledby

```html
<!-- Complex labeling -->
<div role="group" aria-labelledby="billing-label" aria-describedby="billing-desc">
  <h3 id="billing-label">Billing Address</h3>
  <p id="billing-desc">Enter the address associated with your payment method</p>

  <label for="street">Street Address</label>
  <input id="street" type="text" required>

  <label for="city">City</label>
  <input id="city" type="text" required>
</div>

<!-- Error messages -->
<label for="email">Email</label>
<input
  id="email"
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
  required
>
<span id="email-error" role="alert">Please enter a valid email address</span>
```

## Keyboard Navigation

### Keyboard Patterns

```typescript
// Roving tabindex for lists
export function useRovingTabIndex(items: string[]) {
  const [focusedIndex, setFocusedIndex] = useState(0);

  const handleKeyDown = (e: KeyboardEvent, index: number) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setFocusedIndex((index + 1) % items.length);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex((index - 1 + items.length) % items.length);
        break;
      case 'Home':
        e.preventDefault();
        setFocusedIndex(0);
        break;
      case 'End':
        e.preventDefault();
        setFocusedIndex(items.length - 1);
        break;
    }
  };

  return { focusedIndex, handleKeyDown };
}

// Usage
function NavigationList({ items }: { items: string[] }) {
  const { focusedIndex, handleKeyDown } = useRovingTabIndex(items);

  return (
    <ul role="menu">
      {items.map((item, index) => (
        <li key={item} role="none">
          <button
            role="menuitem"
            tabIndex={index === focusedIndex ? 0 : -1}
            onKeyDown={(e) => handleKeyDown(e, index)}
            ref={(el) => {
              if (index === focusedIndex) el?.focus();
            }}
          >
            {item}
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### Grid Navigation

```typescript
// Arrow key navigation for grids
function GridNavigation({ rows, cols, children }: GridNavProps) {
  const [focusedCell, setFocusedCell] = useState({ row: 0, col: 0 });

  const handleKeyDown = (e: KeyboardEvent) => {
    const { row, col } = focusedCell;

    switch (e.key) {
      case 'ArrowRight':
        setFocusedCell({ row, col: Math.min(col + 1, cols - 1) });
        break;
      case 'ArrowLeft':
        setFocusedCell({ row, col: Math.max(col - 1, 0) });
        break;
      case 'ArrowDown':
        setFocusedCell({ row: Math.min(row + 1, rows - 1), col });
        break;
      case 'ArrowUp':
        setFocusedCell({ row: Math.max(row - 1, 0), col });
        break;
    }
  };

  return (
    <div role="grid" onKeyDown={handleKeyDown}>
      {children}
    </div>
  );
}
```

## Responsive Accessibility

### Touch Target Sizing

```css
/* Minimum 44x44px touch targets (WCAG 2.1) */
.button,
.link,
.interactive {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Increase tap area without visual size */
.small-button {
  position: relative;
  padding: 8px 12px;
}

.small-button::after {
  content: '';
  position: absolute;
  top: -8px;
  right: -8px;
  bottom: -8px;
  left: -8px;
}
```

### Focus Indicators

```css
/* High contrast focus indicators */
.focus-visible {
  outline: 3px solid var(--focus-color);
  outline-offset: 2px;
}

/* Dark mode focus */
@media (prefers-color-scheme: dark) {
  .focus-visible {
    outline-color: var(--focus-color-dark);
  }
}

/* Focus within containers */
.card:focus-within {
  box-shadow: 0 0 0 3px var(--focus-color);
}
```

## Screen Reader Helpers

### Visually Hidden

```css
/* Hide visually but not from screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Show on focus */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Announcing Changes

```tsx
// Announce dynamic content changes
function useAnnounce() {
  const [announcement, setAnnouncement] = useState('');

  const announce = (message: string) => {
    setAnnouncement('');
    setTimeout(() => setAnnouncement(message), 100);
  };

  return {
    announce,
    announcer: (
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {announcement}
      </div>
    )
  };
}
```

## Testing Accessibility

### Accessibility Checklist

- [ ] All interactive elements are keyboard accessible
- [ ] Tab order follows logical reading order
- [ ] Focus indicators are visible
- [ ] Skip links are provided
- [ ] Landmarks are properly labeled
- [ ] ARIA attributes are correctly used
- [ ] Touch targets meet 44x44px minimum
- [ ] Color contrast meets WCAG standards
- [ ] Content reflows at 400% zoom
- [ ] No horizontal scrolling at 320px width

### Testing Tools

```javascript
// Automated testing with jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('should not have accessibility violations', async () => {
  const { container } = render(<Layout />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Common Patterns

### Responsive Table

```css
/* Accessible responsive table */
@media (max-width: 768px) {
  .table {
    border: 0;
  }

  .table thead {
    border: none;
    clip: rect(0 0 0 0);
    height: 1px;
    margin: -1px;
    overflow: hidden;
    padding: 0;
    position: absolute;
    width: 1px;
  }

  .table tr {
    border-bottom: 3px solid var(--border-color);
    display: block;
    margin-bottom: 1rem;
  }

  .table td {
    border-bottom: 1px solid var(--border-color);
    display: block;
    text-align: right;
  }

  .table td::before {
    content: attr(data-label);
    float: left;
    font-weight: bold;
  }
}
```