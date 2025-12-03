import React, { useMemo } from 'react';
import './DonutChart.css';

export interface DonutChartData {
  /** Segment label */
  label: string;
  /** Segment value */
  value: number;
  /** Optional custom color (uses brand palette by default) */
  color?: string;
}

export interface DonutChartProps {
  /** Chart data segments */
  data: DonutChartData[];
  /** Chart title */
  title?: string;
  /** Chart size in pixels */
  size?: number;
  /** Donut hole size (0-1, where 0.6 = 60% hole) */
  innerRadius?: number;
  /** Show legend */
  showLegend?: boolean;
  /** Show value labels on segments */
  showLabels?: boolean;
  /** Loading state */
  isLoading?: boolean;
  /** Accessible description */
  ariaLabel?: string;
}

// Palo Alto Networks brand colors
const BRAND_COLORS = [
  'var(--color-cyber-orange)',    // #FA582D
  'var(--color-prisma-blue)',     // #00C0E8
  'var(--color-cortex-green)',    // #00CC66
  'var(--color-strata-yellow)',   // #FFCB06
  'var(--color-unit42-red)',      // #C84727
  '#785EF0',                      // Purple accent
];

/**
 * Donut Chart Component
 *
 * Displays a donut chart for composition/breakdown data.
 * Uses Palo Alto Networks brand colors with colorblind-safe palette.
 *
 * @example
 * <DonutChart
 *   title="Attack Sources"
 *   data={[
 *     { label: 'External', value: 45 },
 *     { label: 'Internal', value: 30 },
 *     { label: 'Unknown', value: 25 },
 *   ]}
 * />
 */
export function DonutChart({
  data,
  title,
  size = 200,
  innerRadius = 0.6,
  showLegend = true,
  showLabels = false,
  isLoading = false,
  ariaLabel,
}: DonutChartProps) {
  const total = useMemo(() => data.reduce((sum, d) => sum + d.value, 0), [data]);

  const segments = useMemo(() => {
    let currentAngle = -90; // Start from top

    return data.map((item, index) => {
      const percentage = (item.value / total) * 100;
      const angle = (percentage / 100) * 360;
      const startAngle = currentAngle;
      const endAngle = currentAngle + angle;
      currentAngle = endAngle;

      return {
        ...item,
        percentage,
        startAngle,
        endAngle,
        color: item.color || BRAND_COLORS[index % BRAND_COLORS.length],
      };
    });
  }, [data, total]);

  const polarToCartesian = (
    centerX: number,
    centerY: number,
    radius: number,
    angleInDegrees: number
  ) => {
    const angleInRadians = ((angleInDegrees - 90) * Math.PI) / 180;
    return {
      x: centerX + radius * Math.cos(angleInRadians),
      y: centerY + radius * Math.sin(angleInRadians),
    };
  };

  const describeArc = (
    x: number,
    y: number,
    outerRadius: number,
    innerRadiusVal: number,
    startAngle: number,
    endAngle: number
  ) => {
    const start = polarToCartesian(x, y, outerRadius, endAngle);
    const end = polarToCartesian(x, y, outerRadius, startAngle);
    const innerStart = polarToCartesian(x, y, innerRadiusVal, endAngle);
    const innerEnd = polarToCartesian(x, y, innerRadiusVal, startAngle);

    const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1;

    return [
      'M', start.x, start.y,
      'A', outerRadius, outerRadius, 0, largeArcFlag, 0, end.x, end.y,
      'L', innerEnd.x, innerEnd.y,
      'A', innerRadiusVal, innerRadiusVal, 0, largeArcFlag, 1, innerStart.x, innerStart.y,
      'Z',
    ].join(' ');
  };

  const center = size / 2;
  const outerRadius = size / 2 - 4;
  const innerRadiusVal = outerRadius * innerRadius;

  if (isLoading) {
    return (
      <div className="donut-chart donut-chart--loading" style={{ width: size }}>
        <div className="donut-chart__spinner">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  const chartDescription = ariaLabel ||
    `${title || 'Chart'}: ${segments.map(s => `${s.label} ${s.percentage.toFixed(1)}%`).join(', ')}`;

  return (
    <div className="donut-chart">
      {title && <h3 className="donut-chart__title">{title}</h3>}

      <div className="donut-chart__content">
        <figure
          className="donut-chart__figure"
          role="img"
          aria-label={chartDescription}
        >
          <svg
            width={size}
            height={size}
            viewBox={`0 0 ${size} ${size}`}
            className="donut-chart__svg"
          >
            {segments.map((segment, index) => (
              <path
                key={segment.label}
                d={describeArc(
                  center,
                  center,
                  outerRadius,
                  innerRadiusVal,
                  segment.startAngle + 90,
                  segment.endAngle + 90
                )}
                fill={segment.color}
                className="donut-chart__segment"
                data-label={segment.label}
                data-value={segment.value}
                data-percentage={segment.percentage.toFixed(1)}
              >
                <title>{`${segment.label}: ${segment.value} (${segment.percentage.toFixed(1)}%)`}</title>
              </path>
            ))}

            {/* Center text */}
            <text
              x={center}
              y={center - 8}
              textAnchor="middle"
              className="donut-chart__center-value"
            >
              {total.toLocaleString()}
            </text>
            <text
              x={center}
              y={center + 16}
              textAnchor="middle"
              className="donut-chart__center-label"
            >
              Total
            </text>
          </svg>
        </figure>

        {showLegend && (
          <ul className="donut-chart__legend" aria-label="Chart legend">
            {segments.map((segment) => (
              <li key={segment.label} className="legend__item">
                <span
                  className="legend__color"
                  style={{ backgroundColor: segment.color }}
                  aria-hidden="true"
                />
                <span className="legend__label">{segment.label}</span>
                <span className="legend__value">
                  {segment.value.toLocaleString()}
                </span>
                <span className="legend__percentage">
                  ({segment.percentage.toFixed(1)}%)
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default DonutChart;
