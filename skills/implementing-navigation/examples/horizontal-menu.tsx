/**
 * Responsive Horizontal Navigation Menu
 *
 * Features:
 * - Responsive design with mobile hamburger menu
 * - Keyboard navigation support
 * - ARIA compliance
 * - Active state management
 * - Dropdown submenus
 */

import React, { useState, useRef, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import './horizontal-menu.css';

interface NavItem {
  id: string;
  label: string;
  href: string;
  children?: NavItem[];
  external?: boolean;
  icon?: React.ReactNode;
}

interface HorizontalMenuProps {
  items: NavItem[];
  logo?: React.ReactNode;
  className?: string;
}

export const HorizontalMenu: React.FC<HorizontalMenuProps> = ({
  items,
  logo,
  className = ''
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const menuRef = useRef<HTMLElement>(null);
  const location = useLocation();

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
    setActiveDropdown(null);
  }, [location]);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setActiveDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        setFocusedIndex((prev) => (prev + 1) % items.length);
        break;

      case 'ArrowLeft':
        e.preventDefault();
        setFocusedIndex((prev) => (prev - 1 + items.length) % items.length);
        break;

      case 'ArrowDown':
        if (items[index].children) {
          e.preventDefault();
          setActiveDropdown(items[index].id);
        }
        break;

      case 'Escape':
        e.preventDefault();
        setActiveDropdown(null);
        break;

      case 'Enter':
      case ' ':
        if (items[index].children) {
          e.preventDefault();
          setActiveDropdown(
            activeDropdown === items[index].id ? null : items[index].id
          );
        }
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

  const toggleDropdown = (itemId: string) => {
    setActiveDropdown(activeDropdown === itemId ? null : itemId);
  };

  const renderNavItem = (item: NavItem, index: number) => {
    const hasChildren = item.children && item.children.length > 0;
    const isActive = activeDropdown === item.id;

    if (hasChildren) {
      return (
        <li key={item.id} className="nav-item has-dropdown">
          <button
            className="nav-link dropdown-trigger"
            aria-expanded={isActive}
            aria-haspopup="true"
            aria-controls={`dropdown-${item.id}`}
            onClick={() => toggleDropdown(item.id)}
            onKeyDown={(e) => handleKeyDown(e, index)}
            tabIndex={focusedIndex === index ? 0 : -1}
          >
            {item.icon && <span className="nav-icon">{item.icon}</span>}
            <span>{item.label}</span>
            <svg
              className={`dropdown-arrow ${isActive ? 'open' : ''}`}
              width="12"
              height="8"
              viewBox="0 0 12 8"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M1 1l5 5 5-5" stroke="currentColor" strokeWidth="2" fill="none" />
            </svg>
          </button>

          {isActive && (
            <ul
              id={`dropdown-${item.id}`}
              className="dropdown-menu"
              role="menu"
              aria-label={`${item.label} submenu`}
            >
              {item.children.map((child) => (
                <li key={child.id} role="none">
                  {child.external ? (
                    <a
                      href={child.href}
                      className="dropdown-link"
                      role="menuitem"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {child.label}
                      <span className="sr-only">(opens in new tab)</span>
                    </a>
                  ) : (
                    <NavLink
                      to={child.href}
                      className={({ isActive }) =>
                        `dropdown-link ${isActive ? 'active' : ''}`
                      }
                      role="menuitem"
                    >
                      {child.label}
                    </NavLink>
                  )}
                </li>
              ))}
            </ul>
          )}
        </li>
      );
    }

    return (
      <li key={item.id} className="nav-item">
        {item.external ? (
          <a
            href={item.href}
            className="nav-link"
            target="_blank"
            rel="noopener noreferrer"
            tabIndex={focusedIndex === index ? 0 : -1}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {item.icon && <span className="nav-icon">{item.icon}</span>}
            <span>{item.label}</span>
          </a>
        ) : (
          <NavLink
            to={item.href}
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            tabIndex={focusedIndex === index ? 0 : -1}
            onKeyDown={(e) => handleKeyDown(e, index)}
            aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
          >
            {item.icon && <span className="nav-icon">{item.icon}</span>}
            <span>{item.label}</span>
          </NavLink>
        )}
      </li>
    );
  };

  return (
    <nav
      ref={menuRef}
      className={`horizontal-menu ${className}`}
      aria-label="Main navigation"
    >
      <div className="nav-container">
        {logo && (
          <div className="nav-logo">
            <NavLink to="/" aria-label="Home">
              {logo}
            </NavLink>
          </div>
        )}

        {/* Desktop Navigation */}
        <ul className="nav-list desktop-nav" role="menubar">
          {items.map((item, index) => renderNavItem(item, index))}
        </ul>

        {/* Mobile Menu Toggle */}
        <button
          className={`mobile-menu-toggle ${mobileMenuOpen ? 'open' : ''}`}
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileMenuOpen}
          aria-controls="mobile-nav"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <span className="hamburger">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        {/* Mobile Navigation */}
        <div
          id="mobile-nav"
          className={`mobile-nav ${mobileMenuOpen ? 'open' : ''}`}
          aria-hidden={!mobileMenuOpen}
        >
          <ul className="nav-list" role="menubar">
            {items.map((item, index) => renderNavItem(item, index))}
          </ul>
        </div>
      </div>
    </nav>
  );
};

// Example usage
export const HorizontalMenuExample: React.FC = () => {
  const navigationItems: NavItem[] = [
    {
      id: 'home',
      label: 'Home',
      href: '/',
      icon: '🏠'
    },
    {
      id: 'products',
      label: 'Products',
      href: '/products',
      icon: '📦',
      children: [
        {
          id: 'electronics',
          label: 'Electronics',
          href: '/products/electronics'
        },
        {
          id: 'clothing',
          label: 'Clothing',
          href: '/products/clothing'
        },
        {
          id: 'books',
          label: 'Books',
          href: '/products/books'
        }
      ]
    },
    {
      id: 'services',
      label: 'Services',
      href: '/services',
      icon: '⚡',
      children: [
        {
          id: 'consulting',
          label: 'Consulting',
          href: '/services/consulting'
        },
        {
          id: 'support',
          label: 'Support',
          href: '/services/support'
        }
      ]
    },
    {
      id: 'about',
      label: 'About',
      href: '/about',
      icon: 'ℹ️'
    },
    {
      id: 'contact',
      label: 'Contact',
      href: '/contact',
      icon: '📧'
    }
  ];

  return (
    <HorizontalMenu
      items={navigationItems}
      logo={<img src="/logo.svg" alt="Company Logo" />}
    />
  );
};