# Accessibility Patterns for Feedback Components

## Overview

Ensuring feedback components are accessible means they can be perceived, understood, and interacted with by all users, including those using assistive technologies.

## ARIA Live Regions

### Understanding Live Regions
```html
<!-- aria-live values -->
<div aria-live="off">      <!-- Not announced (default) -->
<div aria-live="polite">   <!-- Announced when user pauses -->
<div aria-live="assertive"> <!-- Announced immediately -->
```

### Implementation Patterns

#### Toast Notifications
```tsx
function AccessibleToast({ message, type = 'info' }) {
  const ariaLive = type === 'error' ? 'assertive' : 'polite';

  return (
    <div
      role={type === 'error' ? 'alert' : 'status'}
      aria-live={ariaLive}
      aria-atomic="true"
      className={`toast toast-${type}`}
    >
      <span className="toast-icon" aria-hidden="true">
        {getIcon(type)}
      </span>
      <span className="toast-message">{message}</span>
    </div>
  );
}
```

#### Progress Updates
```tsx
function AccessibleProgress({ value, max = 100 }) {
  const percentage = Math.round((value / max) * 100);

  return (
    <>
      {/* Visual progress bar */}
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label="Upload progress"
      >
        <div className="progress-bar" style={{ width: `${percentage}%` }} />
      </div>

      {/* Live region for updates */}
      <div
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {percentage}% complete
      </div>
    </>
  );
}
```

#### Dynamic Content Updates
```tsx
function DynamicContentRegion({ content, priority = 'polite' }) {
  return (
    <div
      aria-live={priority}
      aria-atomic="true"
      aria-relevant="additions removals text"
    >
      {content}
    </div>
  );
}
```

### Custom Announcer Hook
```tsx
function useAnnouncer() {
  const announcerRef = useRef<HTMLDivElement>();

  useEffect(() => {
    // Create announcer element
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    document.body.appendChild(announcer);
    announcerRef.current = announcer;

    return () => {
      document.body.removeChild(announcer);
    };
  }, []);

  const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    if (!announcerRef.current) return;

    // Update aria-live if needed
    announcerRef.current.setAttribute('aria-live', priority);

    // Clear and set message
    announcerRef.current.textContent = '';
    setTimeout(() => {
      if (announcerRef.current) {
        announcerRef.current.textContent = message;
      }
    }, 100);
  }, []);

  return announce;
}

// Usage
function MyComponent() {
  const announce = useAnnouncer();

  const handleSave = async () => {
    try {
      await saveData();
      announce('Changes saved successfully');
    } catch (error) {
      announce('Failed to save changes', 'assertive');
    }
  };
}
```

## Focus Management

### Modal Focus Trap
```tsx
class FocusManager {
  private previousFocus: HTMLElement | null = null;
  private container: HTMLElement;
  private focusableSelectors = [
    'a[href]',
    'button:not([disabled])',
    'textarea:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ];

  constructor(container: HTMLElement) {
    this.container = container;
  }

  trap() {
    // Save current focus
    this.previousFocus = document.activeElement as HTMLElement;

    // Get focusable elements
    const focusableElements = this.getFocusableElements();

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    // Focus first element
    firstElement.focus();

    // Handle Tab navigation
    this.handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    this.container.addEventListener('keydown', this.handleTabKey);
  }

  release() {
    // Remove event listener
    if (this.handleTabKey) {
      this.container.removeEventListener('keydown', this.handleTabKey);
    }

    // Restore focus
    if (this.previousFocus && this.previousFocus.focus) {
      this.previousFocus.focus();
    }
  }

  private getFocusableElements(): HTMLElement[] {
    const selector = this.focusableSelectors.join(',');
    return Array.from(this.container.querySelectorAll(selector));
  }

  private handleTabKey: ((e: KeyboardEvent) => void) | null = null;
}
```

### React Hook for Focus Trap
```tsx
function useFocusTrap(isActive: boolean) {
  const containerRef = useRef<HTMLDivElement>(null);
  const focusManagerRef = useRef<FocusManager>();

  useEffect(() => {
    if (!isActive || !containerRef.current) return;

    const manager = new FocusManager(containerRef.current);
    manager.trap();
    focusManagerRef.current = manager;

    return () => {
      manager.release();
    };
  }, [isActive]);

  return containerRef;
}

// Usage
function Modal({ isOpen, onClose }) {
  const modalRef = useFocusTrap(isOpen);

  return (
    <div ref={modalRef} className="modal">
      {/* Modal content */}
    </div>
  );
}
```

### Focus Restoration
```tsx
function useFocusRestoration() {
  const lastFocusRef = useRef<HTMLElement | null>(null);

  const saveFocus = useCallback(() => {
    lastFocusRef.current = document.activeElement as HTMLElement;
  }, []);

  const restoreFocus = useCallback(() => {
    if (lastFocusRef.current && typeof lastFocusRef.current.focus === 'function') {
      lastFocusRef.current.focus();
    }
  }, []);

  return { saveFocus, restoreFocus };
}
```

## Keyboard Navigation

### Keyboard Shortcut Handler
```tsx
interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  handler: () => void;
}

function useKeyboardShortcuts(shortcuts: KeyboardShortcut[], isActive = true) {
  useEffect(() => {
    if (!isActive) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      shortcuts.forEach(shortcut => {
        const matchesKey = e.key === shortcut.key;
        const matchesCtrl = shortcut.ctrl ? e.ctrlKey || e.metaKey : true;
        const matchesShift = shortcut.shift ? e.shiftKey : true;
        const matchesAlt = shortcut.alt ? e.altKey : true;

        if (matchesKey && matchesCtrl && matchesShift && matchesAlt) {
          e.preventDefault();
          shortcut.handler();
        }
      });
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts, isActive]);
}

// Usage
function NotificationCenter() {
  const [isOpen, setIsOpen] = useState(false);

  useKeyboardShortcuts([
    { key: 'Escape', handler: () => setIsOpen(false) },
    { key: 'n', ctrl: true, handler: () => setIsOpen(true) },
    { key: '/', handler: () => focusSearch() }
  ], isOpen);

  return (
    // Component JSX
  );
}
```

### Roving TabIndex
```tsx
function RovingTabIndex({ items }) {
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

  return (
    <div role="list">
      {items.map((item, index) => (
        <div
          key={item.id}
          role="listitem"
          tabIndex={index === focusedIndex ? 0 : -1}
          onKeyDown={(e) => handleKeyDown(e, index)}
          ref={el => {
            if (index === focusedIndex && el) {
              el.focus();
            }
          }}
        >
          {item.content}
        </div>
      ))}
    </div>
  );
}
```

## Screen Reader Support

### Visually Hidden Content
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Visible on focus (for skip links) */
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

### Screen Reader Announcements
```tsx
function ScreenReaderAnnouncement({ message, priority = 'polite' }) {
  return (
    <div
      role={priority === 'assertive' ? 'alert' : 'status'}
      aria-live={priority}
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );
}
```

### Descriptive Labels
```tsx
function AccessibleButton({ onClick, label, description, icon }) {
  const buttonId = useId();
  const descriptionId = `${buttonId}-description`;

  return (
    <>
      <button
        id={buttonId}
        onClick={onClick}
        aria-label={label}
        aria-describedby={description ? descriptionId : undefined}
      >
        <span aria-hidden="true">{icon}</span>
        <span className="sr-only">{label}</span>
      </button>

      {description && (
        <span id={descriptionId} className="sr-only">
          {description}
        </span>
      )}
    </>
  );
}
```

## ARIA Patterns

### Alert Dialog
```tsx
function AlertDialog({ isOpen, title, message, onConfirm, onCancel }) {
  return (
    <div
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="alert-title"
      aria-describedby="alert-message"
    >
      <h2 id="alert-title">{title}</h2>
      <p id="alert-message">{message}</p>

      <div className="alert-actions">
        <button onClick={onCancel}>Cancel</button>
        <button onClick={onConfirm} autoFocus>Confirm</button>
      </div>
    </div>
  );
}
```

### Status Messages
```tsx
function StatusMessage({ type, message }) {
  const role = type === 'error' ? 'alert' : 'status';
  const ariaLive = type === 'error' ? 'assertive' : 'polite';

  return (
    <div
      role={role}
      aria-live={ariaLive}
      aria-atomic="true"
      className={`status status-${type}`}
    >
      <span className="status-icon" aria-hidden="true">
        {getStatusIcon(type)}
      </span>
      <span className="status-message">{message}</span>
    </div>
  );
}
```

### Loading States
```tsx
function LoadingState({ isLoading, loadingText = 'Loading...' }) {
  return (
    <div
      aria-busy={isLoading}
      aria-live="polite"
      aria-relevant="additions removals"
    >
      {isLoading ? (
        <div role="status">
          <span className="spinner" aria-hidden="true" />
          <span>{loadingText}</span>
        </div>
      ) : (
        <div>Content loaded</div>
      )}
    </div>
  );
}
```

## Color and Contrast

### High Contrast Support
```css
/* Windows High Contrast Mode */
@media (prefers-contrast: high) {
  .toast {
    outline: 2px solid currentColor;
  }

  .modal-overlay {
    background: Canvas;
    opacity: 0.9;
  }

  .progress-bar {
    background: Highlight;
  }
}

/* Forced colors mode */
@media (forced-colors: active) {
  .alert {
    border: 1px solid;
  }

  .btn-primary {
    border: 2px solid;
  }
}
```

### Color Independence
```tsx
function ColorIndependentAlert({ type, message }) {
  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ'
  };

  return (
    <div className={`alert alert-${type}`}>
      {/* Don't rely on color alone */}
      <span className="alert-icon" aria-label={type}>
        {icons[type]}
      </span>
      <span className="alert-type-text sr-only">{type}:</span>
      <span className="alert-message">{message}</span>
    </div>
  );
}
```

## Motion and Animation

### Reduced Motion Support
```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  .toast,
  .modal,
  .progress-bar {
    animation: none !important;
    transition: opacity 0.01ms !important;
  }

  .spinner {
    animation: none;
    border-top-color: transparent;
    border-right-color: var(--spinner-color);
  }
}

/* JavaScript detection */
.reduced-motion .animated-element {
  animation: none;
}
```

### Reduced Motion Hook
```tsx
function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const listener = (e: MediaQueryListEvent) => {
      setPrefersReducedMotion(e.matches);
    };

    mediaQuery.addEventListener('change', listener);
    return () => mediaQuery.removeEventListener('change', listener);
  }, []);

  return prefersReducedMotion;
}

// Usage
function AnimatedToast({ message }) {
  const prefersReducedMotion = usePrefersReducedMotion();

  return (
    <div
      className={`toast ${prefersReducedMotion ? 'no-animation' : 'animated'}`}
    >
      {message}
    </div>
  );
}
```

## Testing Accessibility

### Accessibility Testing Checklist
```typescript
interface AccessibilityTests {
  keyboard: {
    tabNavigation: boolean;
    escapeKey: boolean;
    enterKey: boolean;
    arrowKeys: boolean;
    shortcuts: boolean;
  };
  screenReader: {
    announcements: boolean;
    labels: boolean;
    descriptions: boolean;
    roleAttributes: boolean;
    liveRegions: boolean;
  };
  visual: {
    colorContrast: boolean;
    focusIndicators: boolean;
    textSize: boolean;
    highContrast: boolean;
  };
  interaction: {
    focusTrap: boolean;
    focusRestoration: boolean;
    dismissible: boolean;
    timeouts: boolean;
  };
}
```

### Automated Testing
```tsx
// Using jest-axe for automated accessibility testing
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Toast Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <Toast message="Test message" type="success" />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should announce to screen readers', () => {
    const { getByRole } = render(
      <Toast message="Success" type="success" />
    );

    expect(getByRole('status')).toHaveAttribute('aria-live', 'polite');
  });
});
```

## Best Practices

1. **Always use semantic HTML**: Prefer native elements over ARIA
2. **Test with real assistive technology**: Screen readers, keyboard only
3. **Provide multiple cues**: Don't rely on color or sound alone
4. **Respect user preferences**: Reduced motion, high contrast
5. **Keep focus visible**: Never remove focus indicators
6. **Announce changes**: Use live regions for dynamic content
7. **Manage focus properly**: Trap in modals, restore on close
8. **Provide escape routes**: Always allow keyboard dismissal
9. **Test at different zoom levels**: Ensure 200% zoom works
10. **Document accessibility features**: Help users understand available features