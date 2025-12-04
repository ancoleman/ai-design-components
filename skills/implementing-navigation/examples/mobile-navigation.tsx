import React, { useState } from 'react';
import { Menu, X, Home, User, Settings, LogOut } from 'lucide-react';

/**
 * Mobile Navigation Example
 *
 * Features:
 * - Hamburger menu toggle
 * - Slide-in drawer navigation
 * - Backdrop overlay
 * - Active link highlighting
 * - Accessible (keyboard navigation, ARIA labels)
 */

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { label: 'Home', href: '/', icon: <Home size={20} /> },
  { label: 'Profile', href: '/profile', icon: <User size={20} /> },
  { label: 'Settings', href: '/settings', icon: <Settings size={20} /> },
];

export function MobileNavigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [activePath, setActivePath] = useState('/');

  const toggleMenu = () => setIsOpen(!isOpen);

  const handleNavClick = (href: string) => {
    setActivePath(href);
    setIsOpen(false);
  };

  return (
    <>
      {/* Mobile Header */}
      <header
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          height: '60px',
          backgroundColor: '#fff',
          borderBottom: '1px solid #e0e0e0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 16px',
          zIndex: 1000,
        }}
      >
        <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 600 }}>MyApp</h1>

        <button
          onClick={toggleMenu}
          aria-label="Toggle menu"
          aria-expanded={isOpen}
          aria-controls="mobile-menu"
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </header>

      {/* Backdrop Overlay */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: 1100,
            animation: 'fadeIn 0.3s ease',
          }}
        />
      )}

      {/* Slide-in Drawer */}
      <nav
        id="mobile-menu"
        role="navigation"
        aria-label="Main navigation"
        style={{
          position: 'fixed',
          top: 0,
          right: 0,
          bottom: 0,
          width: '280px',
          maxWidth: '80vw',
          backgroundColor: '#fff',
          boxShadow: '-2px 0 8px rgba(0, 0, 0, 0.1)',
          transform: isOpen ? 'translateX(0)' : 'translateX(100%)',
          transition: 'transform 0.3s ease',
          zIndex: 1200,
          display: 'flex',
          flexDirection: 'column',
          paddingTop: '80px',
        }}
      >
        {/* Navigation Links */}
        <ul
          style={{
            listStyle: 'none',
            margin: 0,
            padding: '0 16px',
            flex: 1,
          }}
        >
          {navItems.map((item) => {
            const isActive = activePath === item.href;

            return (
              <li key={item.href} style={{ marginBottom: '8px' }}>
                <a
                  href={item.href}
                  onClick={(e) => {
                    e.preventDefault();
                    handleNavClick(item.href);
                  }}
                  aria-current={isActive ? 'page' : undefined}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    textDecoration: 'none',
                    color: isActive ? '#2563eb' : '#333',
                    backgroundColor: isActive ? '#eff6ff' : 'transparent',
                    fontWeight: isActive ? 600 : 400,
                    transition: 'all 0.2s ease',
                  }}
                >
                  {item.icon}
                  {item.label}
                </a>
              </li>
            );
          })}
        </ul>

        {/* Footer Action */}
        <div
          style={{
            borderTop: '1px solid #e0e0e0',
            padding: '16px',
          }}
        >
          <button
            onClick={() => console.log('Logout')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              width: '100%',
              padding: '12px 16px',
              backgroundColor: 'transparent',
              border: 'none',
              borderRadius: '8px',
              color: '#ef4444',
              fontWeight: 600,
              cursor: 'pointer',
              textAlign: 'left',
            }}
          >
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </nav>

      {/* Inline styles for animations */}
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `}</style>
    </>
  );
}

export default MobileNavigation;
