import React, { useState, useEffect } from 'react';

/**
 * Complete Admin Dashboard Layout with Sidebar
 * Features: Collapsible sidebar, responsive design, accessible navigation
 */

interface AdminLayoutProps {
  children: React.ReactNode;
  user?: {
    name: string;
    avatar?: string;
  };
}

interface NavItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  href: string;
  badge?: number;
  children?: NavItem[];
}

const navigationItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', href: '/', icon: '📊' },
  { id: 'users', label: 'Users', href: '/users', icon: '👥', badge: 3 },
  {
    id: 'content',
    label: 'Content',
    href: '/content',
    icon: '📝',
    children: [
      { id: 'posts', label: 'Posts', href: '/content/posts' },
      { id: 'media', label: 'Media', href: '/content/media' },
      { id: 'pages', label: 'Pages', href: '/content/pages' },
    ]
  },
  { id: 'analytics', label: 'Analytics', href: '/analytics', icon: '📈' },
  { id: 'settings', label: 'Settings', href: '/settings', icon: '⚙️' },
];

export function AdminLayout({ children, user }: AdminLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  const [currentPath, setCurrentPath] = useState('/');

  // Handle responsive behavior
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setSidebarOpen(false);
      } else {
        setMobileSidebarOpen(false);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Toggle expanded state for nav items with children
  const toggleExpanded = (itemId: string) => {
    setExpandedItems(prev => {
      const next = new Set(prev);
      if (next.has(itemId)) {
        next.delete(itemId);
      } else {
        next.add(itemId);
      }
      return next;
    });
  };

  // Render navigation item
  const renderNavItem = (item: NavItem, depth = 0) => {
    const isActive = currentPath === item.href;
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.has(item.id);

    return (
      <li key={item.id} role="none">
        <a
          href={item.href}
          onClick={(e) => {
            if (hasChildren) {
              e.preventDefault();
              toggleExpanded(item.id);
            } else {
              setCurrentPath(item.href);
            }
          }}
          className={`
            nav-item
            ${isActive ? 'nav-item--active' : ''}
            ${depth > 0 ? 'nav-item--nested' : ''}
          `}
          aria-current={isActive ? 'page' : undefined}
          aria-expanded={hasChildren ? isExpanded : undefined}
        >
          {item.icon && (
            <span className="nav-item__icon" aria-hidden="true">
              {item.icon}
            </span>
          )}
          <span className={`nav-item__label ${!sidebarOpen && depth === 0 ? 'sr-only' : ''}`}>
            {item.label}
          </span>
          {item.badge && (
            <span className="nav-item__badge" aria-label={`${item.badge} new items`}>
              {item.badge}
            </span>
          )}
          {hasChildren && (
            <span
              className="nav-item__chevron"
              aria-hidden="true"
              style={{ transform: isExpanded ? 'rotate(90deg)' : 'rotate(0)' }}
            >
              ›
            </span>
          )}
        </a>
        {hasChildren && isExpanded && (
          <ul className="nav-submenu" role="group">
            {item.children!.map(child => renderNavItem(child, depth + 1))}
          </ul>
        )}
      </li>
    );
  };

  return (
    <div className="admin-layout">
      {/* Skip Links */}
      <a href="#main" className="skip-link">Skip to main content</a>
      <a href="#nav" className="skip-link">Skip to navigation</a>

      {/* Header */}
      <header className="admin-header" role="banner">
        <div className="admin-header__left">
          <button
            className="menu-toggle"
            onClick={() => {
              if (window.innerWidth < 1024) {
                setMobileSidebarOpen(!mobileSidebarOpen);
              } else {
                setSidebarOpen(!sidebarOpen);
              }
            }}
            aria-label={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
          >
            <span className="menu-toggle__line" />
            <span className="menu-toggle__line" />
            <span className="menu-toggle__line" />
          </button>
          <h1 className="admin-header__title">Admin Dashboard</h1>
        </div>

        <div className="admin-header__right">
          {user && (
            <div className="user-menu">
              <button className="user-menu__trigger" aria-label="User menu">
                {user.avatar ? (
                  <img src={user.avatar} alt="" className="user-menu__avatar" />
                ) : (
                  <span className="user-menu__avatar">👤</span>
                )}
                <span className="user-menu__name">{user.name}</span>
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Mobile Overlay */}
      {mobileSidebarOpen && (
        <div
          className="mobile-overlay"
          onClick={() => setMobileSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        id="nav"
        className={`
          admin-sidebar
          ${sidebarOpen ? 'admin-sidebar--open' : 'admin-sidebar--collapsed'}
          ${mobileSidebarOpen ? 'admin-sidebar--mobile-open' : ''}
        `}
        role="navigation"
        aria-label="Main navigation"
      >
        <nav className="admin-nav">
          <ul role="list" className="nav-list">
            {navigationItems.map(item => renderNavItem(item))}
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main
        id="main"
        className={`
          admin-main
          ${sidebarOpen ? 'admin-main--sidebar-open' : 'admin-main--sidebar-collapsed'}
        `}
        role="main"
      >
        <div className="admin-content">
          {children}
        </div>
      </main>
    </div>
  );
}

// CSS (in a separate file or CSS-in-JS)
const styles = `
.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--color-background);
}

/* Skip Links */
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

/* Header */
.admin-header {
  position: sticky;
  top: 0;
  z-index: 40;
  height: var(--header-height, 64px);
  background: var(--color-surface);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.admin-header__left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.admin-header__title {
  font-size: var(--text-xl);
  font-weight: 600;
  margin: 0;
}

/* Menu Toggle */
.menu-toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 44px;
  height: 44px;
  padding: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background-color 0.2s;
}

.menu-toggle:hover {
  background: var(--color-hover);
}

.menu-toggle__line {
  width: 24px;
  height: 2px;
  background: currentColor;
  transition: transform 0.2s;
}

/* Sidebar */
.admin-sidebar {
  position: fixed;
  left: 0;
  top: var(--header-height, 64px);
  bottom: 0;
  width: var(--sidebar-width, 280px);
  background: var(--color-surface);
  border-right: 1px solid var(--border-color);
  transition: width 0.3s ease, transform 0.3s ease;
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 30;
}

.admin-sidebar--collapsed {
  width: var(--sidebar-collapsed-width, 64px);
}

.admin-sidebar--collapsed .nav-item__label {
  opacity: 0;
  width: 0;
}

.admin-sidebar--collapsed .nav-item__badge,
.admin-sidebar--collapsed .nav-item__chevron,
.admin-sidebar--collapsed .nav-submenu {
  display: none;
}

/* Mobile Sidebar */
@media (max-width: 1023px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar--mobile-open {
    transform: translateX(0);
  }

  .mobile-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 25;
  }
}

/* Navigation */
.nav-list {
  list-style: none;
  padding: var(--spacing-sm);
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--color-text);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background-color 0.2s, color 0.2s;
  position: relative;
  min-height: 44px;
}

.nav-item:hover {
  background: var(--color-hover);
}

.nav-item--active {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: 500;
}

.nav-item--nested {
  padding-left: calc(var(--spacing-md) + 24px);
}

.nav-item__icon {
  flex-shrink: 0;
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.nav-item__label {
  flex: 1;
  transition: opacity 0.3s, width 0.3s;
}

.nav-item__badge {
  background: var(--color-error);
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

.nav-item__chevron {
  transition: transform 0.2s;
}

.nav-submenu {
  list-style: none;
  margin: 0;
  padding: 0;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: var(--sidebar-width, 280px);
  margin-top: var(--header-height, 64px);
  transition: margin-left 0.3s ease;
  min-height: calc(100vh - var(--header-height, 64px));
}

.admin-main--sidebar-collapsed {
  margin-left: var(--sidebar-collapsed-width, 64px);
}

@media (max-width: 1023px) {
  .admin-main {
    margin-left: 0;
  }
}

.admin-content {
  padding: var(--spacing-xl);
  max-width: var(--container-max-width, 1440px);
  margin: 0 auto;
}

/* User Menu */
.user-menu__trigger {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: var(--radius-md);
  min-height: 44px;
}

.user-menu__trigger:hover {
  background: var(--color-hover);
}

.user-menu__avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-menu__name {
  font-weight: 500;
}

/* Screen reader only */
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