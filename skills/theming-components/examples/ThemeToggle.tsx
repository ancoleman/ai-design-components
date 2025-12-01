/**
 * Theme Toggle Component
 *
 * Simple button to toggle between light and dark themes
 */

import { useTheme } from './ThemeProvider';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{
        backgroundColor: 'var(--button-bg-secondary)',
        color: 'var(--button-text-secondary)',
        paddingInline: 'var(--button-padding-inline)',
        paddingBlock: 'var(--button-padding-block)',
        borderRadius: 'var(--button-border-radius)',
        border: '1px solid var(--color-border)',
        fontSize: 'var(--font-size-base)',
        fontWeight: 'var(--font-weight-medium)',
        cursor: 'pointer',
        transition: 'var(--transition-fast)',
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--spacing-xs)'
      }}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
    >
      <span style={{ fontSize: '20px' }}>
        {theme === 'light' ? '🌙' : '☀️'}
      </span>
      <span>
        {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
      </span>
    </button>
  );
}

/**
 * Theme Selector with Multiple Options
 */
export function ThemeSelector() {
  const { theme, setTheme, availableThemes } = useTheme();

  return (
    <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
      {availableThemes.map(t => (
        <button
          key={t.value}
          onClick={() => setTheme(t.value)}
          style={{
            backgroundColor: theme === t.value ? 'var(--button-bg-primary)' : 'var(--button-bg-secondary)',
            color: theme === t.value ? 'var(--button-text-primary)' : 'var(--button-text-secondary)',
            paddingInline: 'var(--spacing-md)',
            paddingBlock: 'var(--spacing-sm)',
            borderRadius: 'var(--button-border-radius)',
            border: theme === t.value ? 'none' : '1px solid var(--color-border)',
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'var(--font-weight-medium)',
            cursor: 'pointer',
            transition: 'var(--transition-fast)'
          }}
          aria-label={`Switch to ${t.label} theme`}
          aria-pressed={theme === t.value}
        >
          <span style={{ marginInlineEnd: 'var(--spacing-xs)' }}>{t.icon}</span>
          {t.label}
        </button>
      ))}
    </div>
  );
}
