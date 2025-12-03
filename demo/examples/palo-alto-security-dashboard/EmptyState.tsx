import React from 'react';
import './EmptyState.css';

export interface EmptyStateProps {
  /** Main heading */
  title: string;
  /** Supporting description */
  description?: string;
  /** Icon or illustration */
  icon?: React.ReactNode;
  /** Primary action button */
  action?: {
    label: string;
    onClick: () => void;
  };
  /** Variant style */
  variant?: 'default' | 'error' | 'no-results';
}

/**
 * Empty State Component
 *
 * Displays when there's no data to show or an error occurred.
 * Follows Palo Alto Networks brand styling.
 *
 * @example
 * <EmptyState
 *   title="No threats detected"
 *   description="Your network is secure. No threats in the selected time period."
 *   icon={<ShieldCheckIcon />}
 * />
 */
export function EmptyState({
  title,
  description,
  icon,
  action,
  variant = 'default',
}: EmptyStateProps) {
  const defaultIcons: Record<string, string> = {
    default: '📊',
    error: '⚠️',
    'no-results': '🔍',
  };

  return (
    <div className={`empty-state empty-state--${variant}`}>
      <div className="empty-state__icon" aria-hidden="true">
        {icon || defaultIcons[variant]}
      </div>

      <h3 className="empty-state__title">{title}</h3>

      {description && (
        <p className="empty-state__description">{description}</p>
      )}

      {action && (
        <button
          className="empty-state__action"
          onClick={action.onClick}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

export default EmptyState;
