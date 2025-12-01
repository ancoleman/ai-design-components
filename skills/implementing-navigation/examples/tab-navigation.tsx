/**
 * Tab Navigation with URL Synchronization
 *
 * Features:
 * - URL parameter synchronization
 * - Keyboard navigation (arrow keys, home, end)
 * - ARIA compliant tab pattern
 * - Lazy loading of tab content
 * - Animated transitions
 * - Responsive design
 */

import React, { useState, useRef, useEffect, Suspense, lazy } from 'react';
import { useSearchParams } from 'react-router-dom';
import './tab-navigation.css';

interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  content: React.ReactNode | (() => React.ReactNode);
  disabled?: boolean;
  badge?: string | number;
  lazy?: boolean;
}

interface TabNavigationProps {
  tabs: Tab[];
  defaultTab?: string;
  urlParam?: string;
  orientation?: 'horizontal' | 'vertical';
  variant?: 'default' | 'pills' | 'underline';
  onTabChange?: (tabId: string) => void;
}

export const TabNavigation: React.FC<TabNavigationProps> = ({
  tabs,
  defaultTab,
  urlParam = 'tab',
  orientation = 'horizontal',
  variant = 'default',
  onTabChange
}) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTabId = searchParams.get(urlParam) || defaultTab || tabs[0]?.id;
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  // Find active tab index
  const activeTabIndex = tabs.findIndex(tab => tab.id === activeTabId);

  // Update URL when tab changes
  const handleTabClick = (tabId: string) => {
    const tab = tabs.find(t => t.id === tabId);
    if (tab?.disabled) return;

    setSearchParams(prev => {
      prev.set(urlParam, tabId);
      return prev;
    });

    onTabChange?.(tabId);
  };

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let newIndex = index;
    const enabledTabs = tabs
      .map((tab, idx) => ({ tab, idx }))
      .filter(({ tab }) => !tab.disabled);

    const currentEnabledIndex = enabledTabs.findIndex(({ idx }) => idx === index);

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
        e.preventDefault();
        if (orientation === 'horizontal' && e.key === 'ArrowDown') return;
        if (orientation === 'vertical' && e.key === 'ArrowRight') return;

        const nextEnabled = enabledTabs[currentEnabledIndex + 1];
        if (nextEnabled) {
          newIndex = nextEnabled.idx;
        } else if (enabledTabs.length > 0) {
          newIndex = enabledTabs[0].idx; // Wrap to first
        }
        break;

      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        if (orientation === 'horizontal' && e.key === 'ArrowUp') return;
        if (orientation === 'vertical' && e.key === 'ArrowLeft') return;

        const prevEnabled = enabledTabs[currentEnabledIndex - 1];
        if (prevEnabled) {
          newIndex = prevEnabled.idx;
        } else if (enabledTabs.length > 0) {
          newIndex = enabledTabs[enabledTabs.length - 1].idx; // Wrap to last
        }
        break;

      case 'Home':
        e.preventDefault();
        if (enabledTabs.length > 0) {
          newIndex = enabledTabs[0].idx;
        }
        break;

      case 'End':
        e.preventDefault();
        if (enabledTabs.length > 0) {
          newIndex = enabledTabs[enabledTabs.length - 1].idx;
        }
        break;

      case 'Enter':
      case ' ':
        e.preventDefault();
        handleTabClick(tabs[index].id);
        return;

      default:
        return;
    }

    setFocusedIndex(newIndex);
    tabRefs.current[newIndex]?.focus();
  };

  // Focus management
  useEffect(() => {
    if (focusedIndex >= 0 && tabRefs.current[focusedIndex]) {
      tabRefs.current[focusedIndex]?.focus();
    }
  }, [focusedIndex]);

  // Render tab content
  const renderTabContent = (tab: Tab) => {
    if (typeof tab.content === 'function') {
      return tab.content();
    }
    return tab.content;
  };

  return (
    <div
      className={`tab-navigation ${orientation} ${variant}`}
      data-orientation={orientation}
    >
      <div
        role="tablist"
        aria-label="Tab navigation"
        aria-orientation={orientation}
        className="tab-list"
      >
        {tabs.map((tab, index) => {
          const isActive = tab.id === activeTabId;
          const isDisabled = tab.disabled;

          return (
            <button
              key={tab.id}
              ref={(el) => (tabRefs.current[index] = el)}
              role="tab"
              id={`tab-${tab.id}`}
              aria-selected={isActive}
              aria-disabled={isDisabled}
              aria-controls={`panel-${tab.id}`}
              tabIndex={isActive ? 0 : -1}
              className={`tab-button ${isActive ? 'active' : ''} ${
                isDisabled ? 'disabled' : ''
              }`}
              onClick={() => handleTabClick(tab.id)}
              onKeyDown={(e) => handleKeyDown(e, index)}
              disabled={isDisabled}
            >
              {tab.icon && <span className="tab-icon">{tab.icon}</span>}
              <span className="tab-label">{tab.label}</span>
              {tab.badge !== undefined && (
                <span className="tab-badge" aria-label={`${tab.badge} items`}>
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      <div className="tab-panels">
        {tabs.map((tab) => {
          const isActive = tab.id === activeTabId;

          return (
            <div
              key={tab.id}
              role="tabpanel"
              id={`panel-${tab.id}`}
              aria-labelledby={`tab-${tab.id}`}
              hidden={!isActive}
              tabIndex={0}
              className={`tab-panel ${isActive ? 'active' : ''}`}
            >
              {tab.lazy ? (
                <Suspense fallback={<TabPanelLoader />}>
                  {isActive && renderTabContent(tab)}
                </Suspense>
              ) : (
                renderTabContent(tab)
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Loading component for lazy tabs
const TabPanelLoader: React.FC = () => (
  <div className="tab-panel-loader">
    <div className="loader-spinner" />
    <p>Loading content...</p>
  </div>
);

// Example lazy-loaded components
const OverviewPanel = lazy(() => import('./panels/OverviewPanel'));
const SettingsPanel = lazy(() => import('./panels/SettingsPanel'));
const AnalyticsPanel = lazy(() => import('./panels/AnalyticsPanel'));

// Example usage
export const TabNavigationExample: React.FC = () => {
  const tabs: Tab[] = [
    {
      id: 'overview',
      label: 'Overview',
      icon: '📊',
      content: <OverviewPanel />,
      lazy: true
    },
    {
      id: 'activity',
      label: 'Activity',
      icon: '📈',
      badge: 12,
      content: (
        <div>
          <h2>Recent Activity</h2>
          <ul>
            <li>User logged in - 2 minutes ago</li>
            <li>File uploaded - 15 minutes ago</li>
            <li>Settings updated - 1 hour ago</li>
          </ul>
        </div>
      )
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: '⚙️',
      content: <SettingsPanel />,
      lazy: true
    },
    {
      id: 'analytics',
      label: 'Analytics',
      icon: '📉',
      content: <AnalyticsPanel />,
      lazy: true
    },
    {
      id: 'disabled',
      label: 'Coming Soon',
      icon: '🔒',
      content: <div>This feature is coming soon!</div>,
      disabled: true
    }
  ];

  return (
    <>
      <h1>Horizontal Tabs Example</h1>
      <TabNavigation
        tabs={tabs}
        defaultTab="overview"
        variant="underline"
        onTabChange={(tabId) => console.log('Tab changed to:', tabId)}
      />

      <h1 style={{ marginTop: '3rem' }}>Vertical Pills Example</h1>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <TabNavigation
          tabs={tabs}
          defaultTab="activity"
          orientation="vertical"
          variant="pills"
          urlParam="vertical-tab"
        />
      </div>
    </>
  );
};

// Scrollable tabs for many items
export const ScrollableTabs: React.FC<{ tabs: Tab[] }> = ({ tabs }) => {
  const [showLeftScroll, setShowLeftScroll] = useState(false);
  const [showRightScroll, setShowRightScroll] = useState(false);
  const tabListRef = useRef<HTMLDivElement>(null);

  const checkScroll = () => {
    if (!tabListRef.current) return;

    const { scrollLeft, scrollWidth, clientWidth } = tabListRef.current;
    setShowLeftScroll(scrollLeft > 0);
    setShowRightScroll(scrollLeft < scrollWidth - clientWidth);
  };

  useEffect(() => {
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, [tabs]);

  const scroll = (direction: 'left' | 'right') => {
    if (!tabListRef.current) return;

    const scrollAmount = 200;
    tabListRef.current.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });

    setTimeout(checkScroll, 300);
  };

  return (
    <div className="scrollable-tabs-container">
      {showLeftScroll && (
        <button
          className="scroll-button left"
          onClick={() => scroll('left')}
          aria-label="Scroll tabs left"
        >
          ←
        </button>
      )}

      <div
        ref={tabListRef}
        className="scrollable-tab-list"
        onScroll={checkScroll}
      >
        <TabNavigation tabs={tabs} />
      </div>

      {showRightScroll && (
        <button
          className="scroll-button right"
          onClick={() => scroll('right')}
          aria-label="Scroll tabs right"
        >
          →
        </button>
      )}
    </div>
  );
};