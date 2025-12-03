import React, { useState, useEffect } from 'react';
import { KPICard } from './KPICard';
import { DonutChart } from './DonutChart';
import { EmptyState } from './EmptyState';
import { ToastProvider, useToast } from './Toast';
import './Dashboard.css';

// Sample security data
const MOCK_DATA = {
  kpis: {
    threatsBlocked: { value: 12847, trend: 15.3 },
    activeIncidents: { value: 23, trend: -8.2 },
    vulnerabilities: { value: 156, trend: 4.1 },
    networkUptime: { value: 99.97, trend: 0.02 },
  },
  attackSources: [
    { label: 'External Network', value: 4521 },
    { label: 'Phishing Attempts', value: 3892 },
    { label: 'Malware', value: 2134 },
    { label: 'Brute Force', value: 1456 },
    { label: 'DDoS', value: 844 },
  ],
};

/**
 * Security Dashboard Component
 *
 * Main dashboard displaying security metrics, threat data, and attack sources.
 * Built with Palo Alto Networks brand styling.
 */
function DashboardContent() {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<typeof MOCK_DATA | null>(null);
  const { success, info } = useToast();

  // Simulate data loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setData(MOCK_DATA);
      setIsLoading(false);
      info('Dashboard loaded', 'Showing data for the last 30 days');
    }, 1500);

    return () => clearTimeout(timer);
  }, [info]);

  const handleRefresh = () => {
    setIsLoading(true);
    setTimeout(() => {
      setData(MOCK_DATA);
      setIsLoading(false);
      success('Data refreshed', 'All metrics updated successfully');
    }, 1000);
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard__header">
        <div className="dashboard__header-content">
          <div className="dashboard__branding">
            <h1 className="dashboard__title">Security Analytics</h1>
            <p className="dashboard__subtitle">Palo Alto Networks Threat Dashboard</p>
          </div>

          <div className="dashboard__actions">
            <ThemeToggle />
            <button
              className="dashboard__refresh"
              onClick={handleRefresh}
              disabled={isLoading}
            >
              {isLoading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard__main">
        {/* KPI Cards */}
        <section className="dashboard__section">
          <h2 className="dashboard__section-title">Key Metrics</h2>
          <div className="dashboard__grid dashboard__grid--kpis">
            <KPICard
              label="Threats Blocked"
              value={data ? data.kpis.threatsBlocked.value.toLocaleString() : '-'}
              trend={data?.kpis.threatsBlocked.trend}
              trendLabel="vs last month"
              severity="info"
              isLoading={isLoading}
            />
            <KPICard
              label="Active Incidents"
              value={data ? data.kpis.activeIncidents.value.toString() : '-'}
              trend={data?.kpis.activeIncidents.trend}
              trendLabel="vs last month"
              severity={data && data.kpis.activeIncidents.value > 20 ? 'high' : 'medium'}
              isLoading={isLoading}
            />
            <KPICard
              label="Vulnerabilities"
              value={data ? data.kpis.vulnerabilities.value.toString() : '-'}
              trend={data?.kpis.vulnerabilities.trend}
              trendLabel="vs last month"
              severity="medium"
              isLoading={isLoading}
            />
            <KPICard
              label="Network Uptime"
              value={data ? `${data.kpis.networkUptime.value}%` : '-'}
              trend={data?.kpis.networkUptime.trend}
              trendLabel="vs last month"
              severity="low"
              isLoading={isLoading}
            />
          </div>
        </section>

        {/* Charts Section */}
        <section className="dashboard__section">
          <h2 className="dashboard__section-title">Threat Analysis</h2>
          <div className="dashboard__grid dashboard__grid--charts">
            {isLoading ? (
              <div className="dashboard__chart-placeholder">
                <div className="spinner" />
              </div>
            ) : data ? (
              <DonutChart
                title="Attack Sources"
                data={data.attackSources}
                size={220}
                showLegend={true}
              />
            ) : (
              <EmptyState
                title="No data available"
                description="Unable to load attack source data"
                variant="error"
                action={{ label: 'Retry', onClick: handleRefresh }}
              />
            )}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="dashboard__footer">
        <p>&copy; 2025 Palo Alto Networks. Generated with AI Design Components.</p>
      </footer>
    </div>
  );
}

/**
 * Theme Toggle Button
 */
function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  return (
    <button
      className="theme-toggle"
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}

/**
 * Dashboard with Toast Provider
 */
export function Dashboard() {
  return (
    <ToastProvider>
      <DashboardContent />
    </ToastProvider>
  );
}

export default Dashboard;
