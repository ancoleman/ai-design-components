/**
 * Token Usage Examples
 *
 * Demonstrates how to properly use design tokens in components
 * Shows both inline styles and CSS approaches
 */

import React from 'react';

/**
 * Example 1: Button Component using inline styles
 */
export function TokenButton({ variant = 'primary', children, ...props }) {
  return (
    <button
      style={{
        // ✅ Use component tokens
        backgroundColor: `var(--button-bg-${variant})`,
        color: `var(--button-text-${variant})`,

        // ✅ Use logical properties for RTL
        paddingInline: 'var(--button-padding-inline)',
        paddingBlock: 'var(--button-padding-block)',

        // ✅ Reference other tokens
        borderRadius: 'var(--button-border-radius)',
        fontSize: 'var(--button-font-size)',
        fontWeight: 'var(--button-font-weight)',
        border: 'none',
        cursor: 'pointer',
        transition: 'var(--transition-fast)',
      }}
      {...props}
    >
      {children}
    </button>
  );
}

/**
 * Example 2: Card Component with all token categories
 */
export function TokenCard({ children }) {
  return (
    <div
      style={{
        // Colors
        backgroundColor: 'var(--color-bg-primary)',
        color: 'var(--color-text-primary)',
        border: '1px solid var(--color-border)',

        // Spacing (logical properties)
        paddingInline: 'var(--spacing-lg)',
        paddingBlock: 'var(--spacing-md)',
        marginBlockEnd: 'var(--spacing-md)',

        // Borders
        borderRadius: 'var(--radius-lg)',

        // Shadows
        boxShadow: 'var(--shadow-md)',

        // Typography
        fontFamily: 'var(--font-sans)',
        fontSize: 'var(--font-size-base)',
        lineHeight: 'var(--line-height-normal)',

        // Motion
        transition: 'var(--transition-normal)',
      }}
    >
      {children}
    </div>
  );
}

/**
 * Example 3: Alert Component with semantic tokens
 */
export function TokenAlert({ type = 'info', children }) {
  return (
    <div
      role="alert"
      style={{
        backgroundColor: `var(--color-${type}-bg)`,
        color: `var(--color-${type})`,
        borderInlineStart: `4px solid var(--color-${type})`,
        paddingInline: 'var(--spacing-md)',
        paddingBlock: 'var(--spacing-sm)',
        borderRadius: 'var(--radius-md)',
        fontSize: 'var(--font-size-sm)',
        marginBlockEnd: 'var(--spacing-md)',
      }}
    >
      {children}
    </div>
  );
}

/**
 * Example 4: Token Reference Demo
 * Shows all token categories in use
 */
export function TokenShowcase() {
  return (
    <div style={{ padding: 'var(--spacing-xl)' }}>
      <h1 style={{
        fontSize: 'var(--font-size-4xl)',
        fontWeight: 'var(--font-weight-bold)',
        color: 'var(--color-text-primary)',
        marginBlockEnd: 'var(--spacing-lg)'
      }}>
        Design Token Showcase
      </h1>

      {/* Colors */}
      <section style={{ marginBlockEnd: 'var(--spacing-xl)' }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Colors
        </h2>
        <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
          <div style={{
            width: '100px',
            height: '100px',
            backgroundColor: 'var(--color-primary)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-text-inverse)',
            fontSize: 'var(--font-size-sm)'
          }}>
            Primary
          </div>
          <div style={{
            width: '100px',
            height: '100px',
            backgroundColor: 'var(--color-success)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-text-inverse)',
            fontSize: 'var(--font-size-sm)'
          }}>
            Success
          </div>
          <div style={{
            width: '100px',
            height: '100px',
            backgroundColor: 'var(--color-warning)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-text-inverse)',
            fontSize: 'var(--font-size-sm)'
          }}>
            Warning
          </div>
          <div style={{
            width: '100px',
            height: '100px',
            backgroundColor: 'var(--color-error)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-text-inverse)',
            fontSize: 'var(--font-size-sm)'
          }}>
            Error
          </div>
        </div>
      </section>

      {/* Spacing */}
      <section style={{ marginBlockEnd: 'var(--spacing-xl)' }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Spacing Scale
        </h2>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 'var(--spacing-xs)' }}>
          {['xs', 'sm', 'md', 'lg', 'xl', '2xl'].map(size => (
            <div key={size} style={{
              width: `var(--spacing-${size})`,
              height: `var(--spacing-${size})`,
              backgroundColor: 'var(--color-primary)',
              borderRadius: 'var(--radius-sm)'
            }} />
          ))}
        </div>
      </section>

      {/* Typography */}
      <section style={{ marginBlockEnd: 'var(--spacing-xl)' }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Typography Scale
        </h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)' }}>
          <p style={{ fontSize: 'var(--font-size-xs)' }}>Extra Small (12px)</p>
          <p style={{ fontSize: 'var(--font-size-sm)' }}>Small (14px)</p>
          <p style={{ fontSize: 'var(--font-size-base)' }}>Base (16px)</p>
          <p style={{ fontSize: 'var(--font-size-lg)' }}>Large (18px)</p>
          <p style={{ fontSize: 'var(--font-size-xl)' }}>Extra Large (20px)</p>
        </div>
      </section>

      {/* Shadows */}
      <section style={{ marginBlockEnd: 'var(--spacing-xl)' }}>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Elevation Shadows
        </h2>
        <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
          {['sm', 'md', 'lg', 'xl'].map(size => (
            <div
              key={size}
              style={{
                width: '120px',
                height: '80px',
                backgroundColor: 'var(--color-bg-primary)',
                borderRadius: 'var(--radius-md)',
                boxShadow: `var(--shadow-${size})`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-secondary)'
              }}
            >
              {size}
            </div>
          ))}
        </div>
      </section>

      {/* Border Radius */}
      <section>
        <h2 style={{
          fontSize: 'var(--font-size-2xl)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBlockEnd: 'var(--spacing-md)'
        }}>
          Border Radius
        </h2>
        <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
          {['sm', 'md', 'lg', 'xl', 'full'].map(size => (
            <div
              key={size}
              style={{
                width: size === 'full' ? '80px' : '80px',
                height: '80px',
                backgroundColor: 'var(--color-primary)',
                borderRadius: `var(--radius-${size})`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-inverse)'
              }}
            >
              {size}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
