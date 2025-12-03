import React from 'react';
import './KPICard.css';

export interface KPICardProps {
  /** Label describing the metric */
  label: string;
  /** Primary metric value to display */
  value: string | number;
  /** Trend percentage (positive = up, negative = down) */
  trend?: number;
  /** Comparison period text */
  trendLabel?: string;
  /** Optional icon component */
  icon?: React.ReactNode;
  /** Loading state */
  isLoading?: boolean;
  /** Severity for security metrics */
  severity?: 'critical' | 'high' | 'medium' | 'low' | 'info';
}

/**
 * KPI Card Component
 *
 * Displays a key performance indicator with optional trend indicator.
 * Designed for Palo Alto Networks security dashboards.
 *
 * @example
 * <KPICard
 *   label="Threats Blocked"
 *   value="12,847"
 *   trend={15.3}
 *   trendLabel="vs last week"
 *   icon={<ShieldIcon />}
 * />
 */
export function KPICard({
  label,
  value,
  trend,
  trendLabel = 'vs last period',
  icon,
  isLoading = false,
  severity,
}: KPICardProps) {
  const getTrendClass = () => {
    if (trend === undefined || trend === 0) return 'trend--neutral';
    return trend > 0 ? 'trend--positive' : 'trend--negative';
  };

  const getTrendIcon = () => {
    if (trend === undefined || trend === 0) return '→';
    return trend > 0 ? '↑' : '↓';
  };

  const getSeverityClass = () => {
    if (!severity) return '';
    return `kpi-card--${severity}`;
  };

  if (isLoading) {
    return (
      <div className="kpi-card kpi-card--loading">
        <div className="kpi-card__spinner" aria-label="Loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <article className={`kpi-card ${getSeverityClass()}`}>
      <header className="kpi-card__header">
        {icon && <span className="kpi-card__icon">{icon}</span>}
        <h3 className="kpi-card__label">{label}</h3>
      </header>

      <div className="kpi-card__body">
        <p className="kpi-card__value">{value}</p>

        {trend !== undefined && (
          <div className={`kpi-card__trend ${getTrendClass()}`}>
            <span className="trend__icon">{getTrendIcon()}</span>
            <span className="trend__value">{Math.abs(trend)}%</span>
            <span className="trend__label">{trendLabel}</span>
          </div>
        )}
      </div>

      {severity && (
        <div className={`kpi-card__severity severity--${severity}`}>
          {severity.toUpperCase()}
        </div>
      )}
    </article>
  );
}

export default KPICard;
