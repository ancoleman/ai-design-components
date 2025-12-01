# Navigation Menu Patterns

## Table of Contents
- [Top Navigation (Horizontal)](#top-navigation-horizontal)
- [Side Navigation (Vertical)](#side-navigation-vertical)
- [Mega Menu](#mega-menu)
- [Mobile Navigation](#mobile-navigation)
- [Navigation States](#navigation-states)

## Top Navigation (Horizontal)

### Basic Structure

```tsx
// React/TypeScript
interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
}

const TopNavigation: React.FC = () => {
  return (
    <nav aria-label="Main navigation" className="top-nav">
      <div className="nav-container">
        <a href="/" className="logo" aria-label="Home">
          <img src="/logo.svg" alt="Company Name" />
        </a>

        <ul className="nav-menu" role="menubar">
          {navItems.map(item => (
            <li key={item.href} role="none">
              <a
                href={item.href}
                role="menuitem"
                aria-current={isActive(item.href) ? 'page' : undefined}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        <button
          className="mobile-menu-toggle"
          aria-label="Menu"
          aria-expanded="false"
          aria-controls="mobile-menu"
        >
          <span className="hamburger"></span>
        </button>
      </div>
    </nav>
  );
};
```

### With Dropdown Menus

```tsx
const DropdownNav: React.FC = () => {
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  return (
    <nav aria-label="Main navigation">
      <ul role="menubar">
        {navItems.map(item => (
          <li key={item.href} role="none">
            {item.children ? (
              <>
                <button
                  role="menuitem"
                  aria-haspopup="true"
                  aria-expanded={openDropdown === item.label}
                  onClick={() => toggleDropdown(item.label)}
                >
                  {item.label}
                  <ChevronIcon />
                </button>

                {openDropdown === item.label && (
                  <ul role="menu" className="dropdown-menu">
                    {item.children.map(child => (
                      <li key={child.href} role="none">
                        <a href={child.href} role="menuitem">
                          {child.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </>
            ) : (
              <a href={item.href} role="menuitem">
                {item.label}
              </a>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};
```

### CSS for Top Navigation

```css
.top-nav {
  --nav-height: 64px;
  position: sticky;
  top: 0;
  z-index: var(--z-index-sticky);
  background: var(--nav-bg);
  border-bottom: 1px solid var(--nav-border-color);
  box-shadow: var(--nav-shadow);
}

.nav-container {
  max-width: var(--max-width);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--nav-height);
  padding: 0 var(--nav-padding);
}

.nav-menu {
  display: flex;
  gap: var(--nav-item-gap);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-menu a {
  display: block;
  padding: var(--nav-item-padding);
  color: var(--nav-item-color);
  text-decoration: none;
  border-radius: var(--nav-item-border-radius);
  transition: background-color 200ms;
}

.nav-menu a:hover {
  background: var(--nav-item-hover-bg);
  color: var(--nav-item-hover-color);
}

.nav-menu a[aria-current="page"] {
  background: var(--nav-item-active-bg);
  color: var(--nav-item-active-color);
  font-weight: var(--nav-item-font-weight-active);
}
```

## Side Navigation (Vertical)

### Collapsible Sidebar

```tsx
interface SideNavProps {
  items: NavItem[];
  collapsed?: boolean;
}

const SideNavigation: React.FC<SideNavProps> = ({ items, collapsed }) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());

  const toggleSection = (label: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(label)) {
      newExpanded.delete(label);
    } else {
      newExpanded.add(label);
    }
    setExpandedSections(newExpanded);
  };

  return (
    <nav
      className={`side-nav ${collapsed ? 'collapsed' : ''}`}
      aria-label="Side navigation"
    >
      <ul role="list">
        {items.map(item => (
          <li key={item.href}>
            {item.children ? (
              <div className="nav-section">
                <button
                  className="nav-section-toggle"
                  aria-expanded={expandedSections.has(item.label)}
                  onClick={() => toggleSection(item.label)}
                >
                  <span>{item.label}</span>
                  <ChevronIcon className="chevron" />
                </button>

                {expandedSections.has(item.label) && (
                  <ul className="nav-section-items" role="list">
                    {item.children.map(child => (
                      <li key={child.href}>
                        <NavLink to={child.href}>
                          {child.label}
                        </NavLink>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ) : (
              <NavLink
                to={item.href}
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                <Icon name={item.icon} />
                {!collapsed && <span>{item.label}</span>}
              </NavLink>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};
```

### Multi-Level Nesting

```tsx
const NestedNavigation: React.FC<{ items: NavItem[]; level?: number }> = ({
  items,
  level = 0
}) => {
  const maxNestingLevel = 3;

  if (level >= maxNestingLevel) {
    console.warn('Maximum nesting level reached');
    return null;
  }

  return (
    <ul
      className={`nav-level-${level}`}
      style={{ paddingLeft: `${level * 16}px` }}
    >
      {items.map(item => (
        <li key={item.href}>
          <NavLink to={item.href}>
            {item.label}
          </NavLink>

          {item.children && (
            <NestedNavigation
              items={item.children}
              level={level + 1}
            />
          )}
        </li>
      ))}
    </ul>
  );
};
```

## Mega Menu

### E-commerce Mega Menu

```tsx
interface MegaMenuItem {
  category: string;
  href: string;
  featured?: boolean;
  image?: string;
  subcategories: {
    label: string;
    href: string;
    items: Array<{ label: string; href: string }>;
  }[];
}

const MegaMenu: React.FC<{ items: MegaMenuItem[] }> = ({ items }) => {
  const [activeCategory, setActiveCategory] = useState<string | null>(null);

  return (
    <nav className="mega-menu" aria-label="Main navigation">
      <ul className="mega-menu-bar" role="menubar">
        {items.map(item => (
          <li key={item.category} role="none">
            <button
              className="mega-menu-trigger"
              aria-expanded={activeCategory === item.category}
              aria-haspopup="true"
              role="menuitem"
              onMouseEnter={() => setActiveCategory(item.category)}
              onClick={() => setActiveCategory(
                activeCategory === item.category ? null : item.category
              )}
            >
              {item.category}
            </button>

            {activeCategory === item.category && (
              <div
                className="mega-menu-panel"
                onMouseLeave={() => setActiveCategory(null)}
              >
                <div className="mega-menu-content">
                  {item.featured && item.image && (
                    <div className="mega-menu-featured">
                      <img src={item.image} alt={item.category} />
                      <a href={item.href}>Shop All {item.category}</a>
                    </div>
                  )}

                  <div className="mega-menu-sections">
                    {item.subcategories.map(sub => (
                      <div key={sub.label} className="mega-menu-section">
                        <h3>
                          <a href={sub.href}>{sub.label}</a>
                        </h3>
                        <ul>
                          {sub.items.map(subItem => (
                            <li key={subItem.href}>
                              <a href={subItem.href}>{subItem.label}</a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};
```

## Mobile Navigation

### Hamburger Menu with Drawer

```tsx
const MobileNavigation: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const drawerRef = useRef<HTMLDivElement>(null);

  // Focus trap for accessibility
  useEffect(() => {
    if (isOpen) {
      const firstFocusable = drawerRef.current?.querySelector<HTMLElement>(
        'a, button, [tabindex]:not([tabindex="-1"])'
      );
      firstFocusable?.focus();
    }
  }, [isOpen]);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  return (
    <>
      <button
        className="hamburger-button"
        aria-label={isOpen ? 'Close menu' : 'Open menu'}
        aria-expanded={isOpen}
        aria-controls="mobile-drawer"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className={`hamburger-icon ${isOpen ? 'open' : ''}`}>
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>

      {/* Backdrop */}
      {isOpen && (
        <div
          className="drawer-backdrop"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Drawer */}
      <div
        ref={drawerRef}
        id="mobile-drawer"
        className={`mobile-drawer ${isOpen ? 'open' : ''}`}
        aria-hidden={!isOpen}
      >
        <nav aria-label="Mobile navigation">
          <ul>
            {navItems.map(item => (
              <li key={item.href}>
                <a
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </>
  );
};
```

### Bottom Navigation Bar

```tsx
const BottomNavigation: React.FC = () => {
  const location = useLocation();

  const bottomNavItems = [
    { icon: 'home', label: 'Home', href: '/' },
    { icon: 'search', label: 'Search', href: '/search' },
    { icon: 'cart', label: 'Cart', href: '/cart', badge: 3 },
    { icon: 'user', label: 'Account', href: '/account' }
  ];

  return (
    <nav className="bottom-nav" aria-label="Mobile navigation">
      <ul>
        {bottomNavItems.map(item => (
          <li key={item.href}>
            <NavLink
              to={item.href}
              className={({ isActive }) => isActive ? 'active' : ''}
              aria-current={location.pathname === item.href ? 'page' : undefined}
            >
              <span className="icon-wrapper">
                <Icon name={item.icon} />
                {item.badge && (
                  <span className="badge" aria-label={`${item.badge} items`}>
                    {item.badge}
                  </span>
                )}
              </span>
              <span className="label">{item.label}</span>
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
};
```

### CSS for Mobile Navigation

```css
/* Bottom Navigation */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--nav-bg);
  border-top: 1px solid var(--nav-border-color);
  z-index: var(--z-index-fixed);
}

.bottom-nav ul {
  display: flex;
  justify-content: space-around;
  padding: 0;
  margin: 0;
  list-style: none;
}

.bottom-nav a {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  color: var(--nav-item-color);
  text-decoration: none;
}

.bottom-nav a.active {
  color: var(--nav-item-active-color);
}

/* Hamburger Icon Animation */
.hamburger-icon {
  display: block;
  width: 24px;
  height: 20px;
  position: relative;
}

.hamburger-icon span {
  display: block;
  position: absolute;
  height: 2px;
  width: 100%;
  background: currentColor;
  transition: transform 250ms, opacity 250ms;
}

.hamburger-icon span:nth-child(1) { top: 0; }
.hamburger-icon span:nth-child(2) { top: 50%; transform: translateY(-50%); }
.hamburger-icon span:nth-child(3) { bottom: 0; }

.hamburger-icon.open span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger-icon.open span:nth-child(2) {
  opacity: 0;
}

.hamburger-icon.open span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Mobile Drawer */
.mobile-drawer {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 280px;
  background: var(--nav-bg);
  transform: translateX(-100%);
  transition: transform 300ms;
  z-index: var(--z-index-modal);
}

.mobile-drawer.open {
  transform: translateX(0);
}

.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: calc(var(--z-index-modal) - 1);
}
```

## Navigation States

### Active State Management

```tsx
// With React Router
import { NavLink } from 'react-router-dom';

const NavigationLink: React.FC<{ to: string; children: ReactNode }> = ({
  to,
  children
}) => {
  return (
    <NavLink
      to={to}
      className={({ isActive, isPending }) =>
        isPending ? "pending" : isActive ? "active" : ""
      }
      aria-current={({ isActive }) => isActive ? "page" : undefined}
    >
      {children}
    </NavLink>
  );
};

// Manual active state
const useActiveRoute = (href: string): boolean => {
  const location = useLocation();

  // Exact match
  if (location.pathname === href) return true;

  // Prefix match for nested routes
  if (href !== '/' && location.pathname.startsWith(href)) return true;

  return false;
};
```

### Hover and Focus States

```css
/* Consistent interaction states */
.nav-link {
  position: relative;
  transition: color 200ms, background-color 200ms;
}

/* Hover state */
.nav-link:hover {
  background: var(--nav-item-hover-bg);
  color: var(--nav-item-hover-color);
}

/* Focus state - visible keyboard navigation */
.nav-link:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Focus visible only for keyboard users */
.nav-link:focus:not(:focus-visible) {
  outline: none;
}

.nav-link:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: var(--nav-item-border-radius);
}

/* Active/Current state */
.nav-link[aria-current="page"],
.nav-link.active {
  background: var(--nav-item-active-bg);
  color: var(--nav-item-active-color);
  font-weight: var(--nav-item-font-weight-active);
}

/* Active with indicator */
.nav-link[aria-current="page"]::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-primary);
}
```

### Loading States

```tsx
const NavigationWithLoading: React.FC = () => {
  const navigation = useNavigation();
  const isNavigating = navigation.state === 'loading';

  return (
    <nav>
      {isNavigating && (
        <div className="nav-progress" role="status" aria-live="polite">
          <span className="sr-only">Loading page...</span>
          <div className="progress-bar" />
        </div>
      )}

      <ul>
        {navItems.map(item => (
          <li key={item.href}>
            <NavLink to={item.href}>
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
};
```

## Responsive Patterns

### Adaptive Navigation

```tsx
const AdaptiveNavigation: React.FC = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  if (isMobile) {
    return <MobileNavigation />;
  }

  return <DesktopNavigation />;
};
```

### Priority+ Navigation

```tsx
// Shows priority items, hides others in "More" menu
const PriorityNavigation: React.FC = () => {
  const [visibleItems, setVisibleItems] = useState(navItems);
  const [overflowItems, setOverflowItems] = useState<NavItem[]>([]);
  const navRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const handleResize = () => {
      if (!navRef.current) return;

      const containerWidth = navRef.current.offsetWidth;
      const itemWidths: number[] = [];
      let totalWidth = 100; // Account for "More" button

      const items = Array.from(navRef.current.querySelectorAll('.nav-item'));
      items.forEach(item => {
        itemWidths.push(item.getBoundingClientRect().width);
      });

      const visible: NavItem[] = [];
      const overflow: NavItem[] = [];

      navItems.forEach((item, i) => {
        if (totalWidth + itemWidths[i] <= containerWidth) {
          visible.push(item);
          totalWidth += itemWidths[i];
        } else {
          overflow.push(item);
        }
      });

      setVisibleItems(visible);
      setOverflowItems(overflow);
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <nav ref={navRef} className="priority-nav">
      <ul>
        {visibleItems.map(item => (
          <li key={item.href} className="nav-item">
            <a href={item.href}>{item.label}</a>
          </li>
        ))}

        {overflowItems.length > 0 && (
          <li className="nav-more">
            <button aria-haspopup="true">
              More
            </button>
            <ul className="overflow-menu">
              {overflowItems.map(item => (
                <li key={item.href}>
                  <a href={item.href}>{item.label}</a>
                </li>
              ))}
            </ul>
          </li>
        )}
      </ul>
    </nav>
  );
};
```