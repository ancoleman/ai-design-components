# Accessible Navigation Patterns

## Table of Contents
- [ARIA Patterns](#aria-patterns)
- [Keyboard Navigation](#keyboard-navigation)
- [Focus Management](#focus-management)
- [Screen Reader Support](#screen-reader-support)
- [Mobile Accessibility](#mobile-accessibility)
- [Testing & Validation](#testing--validation)

## ARIA Patterns

### Navigation Landmarks

```html
<!-- Main navigation with proper ARIA -->
<nav aria-label="Main navigation" role="navigation">
  <ul role="menubar" aria-label="Site sections">
    <li role="none">
      <a role="menuitem" href="/" aria-current="page">Home</a>
    </li>
    <li role="none">
      <button
        role="menuitem"
        aria-haspopup="true"
        aria-expanded="false"
        aria-controls="products-menu"
      >
        Products
        <span aria-hidden="true">▼</span>
      </button>
      <ul role="menu" id="products-menu" aria-label="Products">
        <li role="none">
          <a role="menuitem" href="/products/category1">Category 1</a>
        </li>
        <li role="none">
          <a role="menuitem" href="/products/category2">Category 2</a>
        </li>
      </ul>
    </li>
  </ul>
</nav>

<!-- Secondary navigation -->
<nav aria-label="Breadcrumb" role="navigation">
  <ol aria-label="Breadcrumb trail">
    <li><a href="/">Home</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

<!-- Page navigation -->
<nav aria-label="Pagination" role="navigation">
  <ul>
    <li>
      <a href="?page=1" aria-label="Go to previous page">Previous</a>
    </li>
    <li>
      <a href="?page=1" aria-label="Go to page 1">1</a>
    </li>
    <li>
      <span aria-current="page" aria-label="Current page, page 2">2</span>
    </li>
    <li>
      <a href="?page=3" aria-label="Go to page 3">3</a>
    </li>
    <li>
      <a href="?page=3" aria-label="Go to next page">Next</a>
    </li>
  </ul>
</nav>
```

### Menu ARIA Patterns

```tsx
// React implementation with proper ARIA
interface MenuProps {
  items: MenuItem[];
}

const AccessibleMenu: React.FC<MenuProps> = ({ items }) => {
  const [activeSubmenu, setActiveSubmenu] = useState<string | null>(null);
  const [focusedIndex, setFocusedIndex] = useState<number>(-1);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setFocusedIndex((prev) => Math.min(prev + 1, items.length - 1));
        break;

      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex((prev) => Math.max(prev - 1, 0));
        break;

      case 'ArrowRight':
        if (items[index].children) {
          e.preventDefault();
          setActiveSubmenu(items[index].id);
          // Focus first item in submenu
        }
        break;

      case 'ArrowLeft':
      case 'Escape':
        e.preventDefault();
        setActiveSubmenu(null);
        break;

      case 'Home':
        e.preventDefault();
        setFocusedIndex(0);
        break;

      case 'End':
        e.preventDefault();
        setFocusedIndex(items.length - 1);
        break;

      case ' ':
      case 'Enter':
        e.preventDefault();
        if (items[index].children) {
          setActiveSubmenu(
            activeSubmenu === items[index].id ? null : items[index].id
          );
        } else if (items[index].href) {
          window.location.href = items[index].href;
        }
        break;
    }
  };

  return (
    <ul role="menubar" aria-label="Main navigation">
      {items.map((item, index) => (
        <li key={item.id} role="none">
          {item.children ? (
            <>
              <button
                role="menuitem"
                aria-haspopup="true"
                aria-expanded={activeSubmenu === item.id}
                aria-controls={`submenu-${item.id}`}
                tabIndex={focusedIndex === index ? 0 : -1}
                onKeyDown={(e) => handleKeyDown(e, index)}
                onClick={() => setActiveSubmenu(
                  activeSubmenu === item.id ? null : item.id
                )}
              >
                {item.label}
              </button>

              {activeSubmenu === item.id && (
                <ul
                  role="menu"
                  id={`submenu-${item.id}`}
                  aria-label={`${item.label} submenu`}
                >
                  {item.children.map((child) => (
                    <li key={child.id} role="none">
                      <a role="menuitem" href={child.href} tabIndex={-1}>
                        {child.label}
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </>
          ) : (
            <a
              role="menuitem"
              href={item.href}
              tabIndex={focusedIndex === index ? 0 : -1}
              onKeyDown={(e) => handleKeyDown(e, index)}
              aria-current={isCurrentPage(item.href) ? 'page' : undefined}
            >
              {item.label}
            </a>
          )}
        </li>
      ))}
    </ul>
  );
};
```

### Tab ARIA Pattern

```tsx
const AccessibleTabs: React.FC<{ tabs: Tab[] }> = ({ tabs }) => {
  const [activeTab, setActiveTab] = useState(0);
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let newIndex = index;

    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        newIndex = (index + 1) % tabs.length;
        break;

      case 'ArrowLeft':
        e.preventDefault();
        newIndex = index === 0 ? tabs.length - 1 : index - 1;
        break;

      case 'Home':
        e.preventDefault();
        newIndex = 0;
        break;

      case 'End':
        e.preventDefault();
        newIndex = tabs.length - 1;
        break;

      default:
        return;
    }

    setActiveTab(newIndex);
    tabRefs.current[newIndex]?.focus();
  };

  return (
    <div className="tabs">
      <div role="tablist" aria-label="Tabs">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            ref={(el) => (tabRefs.current[index] = el)}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === index}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeTab === index ? 0 : -1}
            onClick={() => setActiveTab(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map((tab, index) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== index}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
};
```

## Keyboard Navigation

### Key Bindings Reference

```typescript
// Keyboard navigation patterns for different components

const NAVIGATION_KEYS = {
  // Basic navigation
  TAB: 'Tab',
  SHIFT_TAB: 'Shift+Tab',
  ENTER: 'Enter',
  SPACE: ' ',
  ESCAPE: 'Escape',

  // Arrow navigation
  ARROW_UP: 'ArrowUp',
  ARROW_DOWN: 'ArrowDown',
  ARROW_LEFT: 'ArrowLeft',
  ARROW_RIGHT: 'ArrowRight',

  // Jump navigation
  HOME: 'Home',
  END: 'End',
  PAGE_UP: 'PageUp',
  PAGE_DOWN: 'PageDown'
};

// Component-specific patterns
const KEYBOARD_PATTERNS = {
  menubar: {
    [NAVIGATION_KEYS.ARROW_RIGHT]: 'Next menu item',
    [NAVIGATION_KEYS.ARROW_LEFT]: 'Previous menu item',
    [NAVIGATION_KEYS.ARROW_DOWN]: 'Open submenu or next item',
    [NAVIGATION_KEYS.ARROW_UP]: 'Previous item',
    [NAVIGATION_KEYS.HOME]: 'First menu item',
    [NAVIGATION_KEYS.END]: 'Last menu item',
    [NAVIGATION_KEYS.ENTER]: 'Activate menu item',
    [NAVIGATION_KEYS.SPACE]: 'Activate menu item',
    [NAVIGATION_KEYS.ESCAPE]: 'Close submenu'
  },

  tabs: {
    [NAVIGATION_KEYS.ARROW_RIGHT]: 'Next tab',
    [NAVIGATION_KEYS.ARROW_LEFT]: 'Previous tab',
    [NAVIGATION_KEYS.HOME]: 'First tab',
    [NAVIGATION_KEYS.END]: 'Last tab',
    [NAVIGATION_KEYS.ENTER]: 'Activate tab (if not automatic)',
    [NAVIGATION_KEYS.SPACE]: 'Activate tab (if not automatic)'
  },

  breadcrumb: {
    [NAVIGATION_KEYS.TAB]: 'Next breadcrumb item',
    [NAVIGATION_KEYS.SHIFT_TAB]: 'Previous breadcrumb item',
    [NAVIGATION_KEYS.ENTER]: 'Navigate to breadcrumb'
  },

  pagination: {
    [NAVIGATION_KEYS.TAB]: 'Next pagination control',
    [NAVIGATION_KEYS.SHIFT_TAB]: 'Previous pagination control',
    [NAVIGATION_KEYS.ENTER]: 'Navigate to page',
    [NAVIGATION_KEYS.ARROW_RIGHT]: 'Next page (optional)',
    [NAVIGATION_KEYS.ARROW_LEFT]: 'Previous page (optional)'
  }
};
```

### Roving Tabindex Implementation

```tsx
// Hook for implementing roving tabindex
const useRovingTabindex = (items: any[], loop = true) => {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const refs = useRef<(HTMLElement | null)[]>([]);

  useEffect(() => {
    refs.current = refs.current.slice(0, items.length);
  }, [items]);

  const handleKeyDown = (e: React.KeyboardEvent, currentIndex: number) => {
    let nextIndex = currentIndex;

    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        e.preventDefault();
        if (currentIndex < items.length - 1) {
          nextIndex = currentIndex + 1;
        } else if (loop) {
          nextIndex = 0;
        }
        break;

      case 'ArrowUp':
      case 'ArrowLeft':
        e.preventDefault();
        if (currentIndex > 0) {
          nextIndex = currentIndex - 1;
        } else if (loop) {
          nextIndex = items.length - 1;
        }
        break;

      case 'Home':
        e.preventDefault();
        nextIndex = 0;
        break;

      case 'End':
        e.preventDefault();
        nextIndex = items.length - 1;
        break;

      default:
        return;
    }

    setFocusedIndex(nextIndex);
    refs.current[nextIndex]?.focus();
  };

  const getTabIndex = (index: number) => {
    return index === focusedIndex ? 0 : -1;
  };

  const setRef = (index: number) => (el: HTMLElement | null) => {
    refs.current[index] = el;
  };

  return {
    focusedIndex,
    handleKeyDown,
    getTabIndex,
    setRef
  };
};

// Usage example
const NavigationList: React.FC = () => {
  const items = ['Home', 'Products', 'About', 'Contact'];
  const { focusedIndex, handleKeyDown, getTabIndex, setRef } = useRovingTabindex(items);

  return (
    <ul role="list">
      {items.map((item, index) => (
        <li key={item}>
          <a
            ref={setRef(index)}
            href={`#${item.toLowerCase()}`}
            tabIndex={getTabIndex(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
            aria-current={focusedIndex === index ? 'true' : undefined}
          >
            {item}
          </a>
        </li>
      ))}
    </ul>
  );
};
```

## Focus Management

### Skip Navigation Link

```tsx
const SkipToContent: React.FC = () => {
  return (
    <>
      <a
        href="#main-content"
        className="skip-link"
        onClick={(e) => {
          e.preventDefault();
          const main = document.getElementById('main-content');
          main?.focus();
          main?.scrollIntoView();
        }}
      >
        Skip to main content
      </a>

      <style jsx>{`
        .skip-link {
          position: absolute;
          top: -40px;
          left: 0;
          background: var(--color-primary);
          color: white;
          padding: 8px 16px;
          text-decoration: none;
          z-index: 100;
          border-radius: 0 0 4px 0;
        }

        .skip-link:focus {
          top: 0;
        }
      `}</style>
    </>
  );
};
```

### Focus Trap for Modals/Drawers

```tsx
const useFocusTrap = (isActive: boolean) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isActive) {
      // Store previous focus
      previousFocus.current = document.activeElement as HTMLElement;

      // Get focusable elements
      const getFocusableElements = () => {
        if (!containerRef.current) return [];

        const focusableSelectors = [
          'a[href]',
          'button:not([disabled])',
          'input:not([disabled])',
          'select:not([disabled])',
          'textarea:not([disabled])',
          '[tabindex]:not([tabindex="-1"])'
        ].join(', ');

        return Array.from(
          containerRef.current.querySelectorAll<HTMLElement>(focusableSelectors)
        );
      };

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key !== 'Tab') return;

        const focusableElements = getFocusableElements();
        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          // Shift + Tab
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          // Tab
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      };

      // Focus first element
      const focusableElements = getFocusableElements();
      if (focusableElements.length > 0) {
        focusableElements[0].focus();
      }

      document.addEventListener('keydown', handleKeyDown);

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        // Restore focus
        previousFocus.current?.focus();
      };
    }
  }, [isActive]);

  return containerRef;
};

// Usage
const Modal: React.FC<{ isOpen: boolean; onClose: () => void }> = ({
  isOpen,
  onClose,
  children
}) => {
  const focusTrapRef = useFocusTrap(isOpen);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        ref={focusTrapRef}
        className="modal-content"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          className="close-button"
          onClick={onClose}
          aria-label="Close modal"
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
};
```

### Focus Indicators

```css
/* Visible focus indicators */
:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove default outline, add custom */
a:focus,
button:focus,
input:focus,
select:focus,
textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-background),
              0 0 0 4px var(--color-primary);
}

/* Focus visible - only show focus on keyboard navigation */
:focus:not(:focus-visible) {
  outline: none;
  box-shadow: none;
}

:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :focus {
    outline: 3px solid currentColor;
    outline-offset: 2px;
  }
}

/* Forced colors mode (Windows High Contrast) */
@media (forced-colors: active) {
  :focus {
    outline: 3px solid currentColor;
  }
}
```

## Screen Reader Support

### Announcing Navigation Changes

```tsx
// Live region for route changes
const RouteAnnouncer: React.FC = () => {
  const location = useLocation();
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    // Get page title or route name
    const pageTitle = document.title || 'New page';
    setAnnouncement(`Navigated to ${pageTitle}`);

    // Clear announcement after screen reader reads it
    const timer = setTimeout(() => {
      setAnnouncement('');
    }, 1000);

    return () => clearTimeout(timer);
  }, [location]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  );
};

// CSS for screen reader only content
const srOnlyStyles = `
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
`;
```

### Descriptive Labels

```tsx
// Proper labeling for navigation elements
const NavigationWithLabels: React.FC = () => {
  return (
    <nav aria-label="Main navigation">
      {/* Icon-only buttons need labels */}
      <button aria-label="Open menu">
        <MenuIcon aria-hidden="true" />
      </button>

      {/* Current page indicator */}
      <a href="/home" aria-current="page">
        Home
        <span className="sr-only">(current page)</span>
      </a>

      {/* Badge with context */}
      <a href="/cart">
        Cart
        <span className="badge" aria-label="3 items in cart">
          3
        </span>
      </a>

      {/* Loading state */}
      <div role="status" aria-label="Loading navigation">
        <Spinner />
        <span className="sr-only">Loading navigation items...</span>
      </div>

      {/* Search with proper labeling */}
      <form role="search" aria-label="Site search">
        <label htmlFor="search-input" className="sr-only">
          Search the site
        </label>
        <input
          id="search-input"
          type="search"
          placeholder="Search..."
          aria-describedby="search-hint"
        />
        <span id="search-hint" className="sr-only">
          Press Enter to search
        </span>
      </form>
    </nav>
  );
};
```

## Mobile Accessibility

### Touch Target Sizes

```css
/* Minimum touch target size: 44x44px (iOS) or 48x48px (Android) */
.nav-link,
.nav-button {
  min-height: 44px;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
}

/* Ensure adequate spacing between targets */
.nav-list {
  display: flex;
  gap: 8px; /* Minimum 8px between targets */
}

/* Mobile-specific adjustments */
@media (max-width: 768px) {
  .nav-link,
  .nav-button {
    min-height: 48px;
    min-width: 48px;
    font-size: 16px; /* Prevent zoom on iOS */
  }
}
```

### Gesture Alternatives

```tsx
// Swipe navigation with keyboard alternative
const SwipeableNavigation: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const pages = ['Page 1', 'Page 2', 'Page 3'];

  const goToNext = () => {
    setCurrentIndex((prev) => Math.min(prev + 1, pages.length - 1));
  };

  const goToPrevious = () => {
    setCurrentIndex((prev) => Math.max(prev - 1, 0));
  };

  const handlers = useSwipeable({
    onSwipedLeft: goToNext,
    onSwipedRight: goToPrevious,
    preventDefaultTouchmoveEvent: true,
    trackMouse: true
  });

  return (
    <div {...handlers} role="region" aria-label="Swipeable content">
      {/* Current page */}
      <div aria-live="polite">
        {pages[currentIndex]}
      </div>

      {/* Keyboard-accessible controls */}
      <div className="navigation-controls">
        <button
          onClick={goToPrevious}
          disabled={currentIndex === 0}
          aria-label="Go to previous page"
        >
          Previous
        </button>

        <span aria-label={`Page ${currentIndex + 1} of ${pages.length}`}>
          {currentIndex + 1} / {pages.length}
        </span>

        <button
          onClick={goToNext}
          disabled={currentIndex === pages.length - 1}
          aria-label="Go to next page"
        >
          Next
        </button>
      </div>
    </div>
  );
};
```

## Testing & Validation

### Accessibility Testing Checklist

```typescript
// Automated testing with jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Navigation Accessibility', () => {
  test('should have no WCAG violations', async () => {
    const { container } = render(<Navigation />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('should have proper ARIA attributes', () => {
    const { getByRole } = render(<Navigation />);

    const nav = getByRole('navigation');
    expect(nav).toHaveAttribute('aria-label');

    const menubar = getByRole('menubar');
    expect(menubar).toBeInTheDocument();

    const menuitems = getAllByRole('menuitem');
    menuitems.forEach((item) => {
      if (item.getAttribute('aria-haspopup')) {
        expect(item).toHaveAttribute('aria-expanded');
      }
    });
  });

  test('should support keyboard navigation', () => {
    const { getAllByRole } = render(<Navigation />);
    const items = getAllByRole('menuitem');

    // Focus first item
    items[0].focus();
    expect(document.activeElement).toBe(items[0]);

    // Arrow right moves to next
    fireEvent.keyDown(items[0], { key: 'ArrowRight' });
    expect(document.activeElement).toBe(items[1]);

    // Arrow left moves to previous
    fireEvent.keyDown(items[1], { key: 'ArrowLeft' });
    expect(document.activeElement).toBe(items[0]);
  });
});

// Manual testing checklist
const ACCESSIBILITY_TESTS = {
  keyboard: [
    'Can navigate entire menu with keyboard only',
    'Tab order is logical',
    'Focus indicators are visible',
    'Can activate all interactive elements',
    'Escape key closes submenus',
    'No keyboard traps'
  ],

  screenReader: [
    'All navigation items are announced',
    'Current page is identified',
    'Menu structure is conveyed',
    'State changes are announced',
    'Landmarks are properly labeled'
  ],

  mobile: [
    'Touch targets are at least 44x44px',
    'Adequate spacing between targets',
    'Works with screen reader gestures',
    'Hamburger menu is accessible'
  ],

  wcag: [
    'Meets color contrast requirements (4.5:1)',
    'Focus indicators meet contrast requirements (3:1)',
    'Text can be resized to 200% without loss of functionality',
    'Works without JavaScript',
    'Proper heading hierarchy'
  ]
};
```

### Browser Testing Tools

```javascript
// Accessibility testing script
const testNavigationAccessibility = () => {
  // Check for skip links
  const skipLinks = document.querySelectorAll('a[href^="#"]');
  console.log(`Found ${skipLinks.length} skip links`);

  // Check ARIA labels
  const unlabeledNavs = document.querySelectorAll('nav:not([aria-label])');
  if (unlabeledNavs.length > 0) {
    console.warn('Found navigation elements without aria-label:', unlabeledNavs);
  }

  // Check focus order
  const focusableElements = document.querySelectorAll(
    'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  let tabIndexes = [];
  focusableElements.forEach((el) => {
    const tabIndex = el.getAttribute('tabindex');
    if (tabIndex && parseInt(tabIndex) > 0) {
      tabIndexes.push({ element: el, tabIndex });
    }
  });

  if (tabIndexes.length > 0) {
    console.warn('Found elements with positive tabindex (avoid):', tabIndexes);
  }

  // Check color contrast
  const checkContrast = (foreground, background) => {
    // Simplified contrast calculation
    const getLuminance = (color) => {
      // Convert color to luminance
      return 0.5; // Placeholder
    };

    const ratio = (Math.max(getLuminance(foreground), getLuminance(background)) + 0.05) /
                  (Math.min(getLuminance(foreground), getLuminance(background)) + 0.05);

    return ratio >= 4.5; // WCAG AA standard
  };

  console.log('Accessibility check complete');
};
```