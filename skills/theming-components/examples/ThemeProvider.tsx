/**
 * React Theme Provider
 *
 * Provides theme context to entire application with:
 * - Light/dark mode support
 * - Custom theme support
 * - LocalStorage persistence
 * - System preference detection
 * - FOUC prevention
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type Theme = 'light' | 'dark' | 'high-contrast' | string;

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  availableThemes: { value: Theme; label: string; icon: string }[];
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const AVAILABLE_THEMES = [
  { value: 'light' as Theme, label: 'Light', icon: '☀️' },
  { value: 'dark' as Theme, label: 'Dark', icon: '🌙' },
  { value: 'high-contrast' as Theme, label: 'High Contrast', icon: '⚡' }
];

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>('light');
  const [isInitialized, setIsInitialized] = useState(false);

  // Initialize theme on mount
  useEffect(() => {
    const initTheme = () => {
      // 1. Check saved preference
      const saved = localStorage.getItem('theme');
      if (saved) {
        setThemeState(saved);
        return;
      }

      // 2. Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const prefersHighContrast = window.matchMedia('(prefers-contrast: high)').matches;

      if (prefersHighContrast) {
        setThemeState('high-contrast');
      } else if (prefersDark) {
        setThemeState('dark');
      } else {
        setThemeState('light');
      }
    };

    initTheme();
    setIsInitialized(true);
  }, []);

  // Apply theme when it changes
  useEffect(() => {
    if (!isInitialized) return;

    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme, isInitialized]);

  // Listen to system preference changes
  useEffect(() => {
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const contrastQuery = window.matchMedia('(prefers-contrast: high)');

    const handleChange = () => {
      // Only auto-switch if user hasn't set manual preference
      if (!localStorage.getItem('theme')) {
        if (contrastQuery.matches) {
          setThemeState('high-contrast');
        } else if (darkModeQuery.matches) {
          setThemeState('dark');
        } else {
          setThemeState('light');
        }
      }
    };

    darkModeQuery.addEventListener('change', handleChange);
    contrastQuery.addEventListener('change', handleChange);

    return () => {
      darkModeQuery.removeEventListener('change', handleChange);
      contrastQuery.removeEventListener('change', handleChange);
    };
  }, []);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  const toggleTheme = () => {
    setThemeState(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme, availableThemes: AVAILABLE_THEMES }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
