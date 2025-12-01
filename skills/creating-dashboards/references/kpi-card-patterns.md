# KPI Card Design Patterns

## Table of Contents
- [Essential Elements](#essential-elements)
- [Number Formatting](#number-formatting)
- [Trend Indicators](#trend-indicators)
- [Sparkline Integration](#sparkline-integration)
- [Card Variations](#card-variations)
- [Interactive Features](#interactive-features)
- [Accessibility](#accessibility)

## Essential Elements

### Basic KPI Card Structure
```tsx
interface KPICard {
  label: string;           // "Monthly Revenue"
  value: number;          // 1245832
  unit?: string;          // "$", "%", "users"
  trend?: {
    direction: 'up' | 'down' | 'neutral';
    value: number;        // 15.3
    comparison: string;   // "vs last month"
  };
  sparkline?: number[];   // [100, 120, 115, 140, 155]
  status?: 'success' | 'warning' | 'error' | 'neutral';
  icon?: ReactNode;
  onClick?: () => void;
}
```

### Visual Hierarchy
```
┌──────────────────────────────┐
│ 👥 Active Users     [ℹ️] [⚙️] │ ← Icon, Label, Actions
│                              │
│         12,543               │ ← Primary Value (largest)
│                              │
│   ↑ 234 (+1.9%)             │ ← Change (medium)
│   vs yesterday               │ ← Comparison (small)
│                              │
│   ▂▃▅▄▆▇█▆▅ Last 7 days     │ ← Sparkline + Period
└──────────────────────────────┘
```

## Number Formatting

### Large Number Abbreviation
```typescript
function formatLargeNumber(value: number): string {
  const abbreviations = [
    { threshold: 1e9, suffix: 'B' },
    { threshold: 1e6, suffix: 'M' },
    { threshold: 1e3, suffix: 'K' }
  ];

  for (const { threshold, suffix } of abbreviations) {
    if (Math.abs(value) >= threshold) {
      const formatted = (value / threshold).toFixed(1);
      return `${formatted}${suffix}`;
    }
  }

  return value.toLocaleString();
}

// Examples:
// 1234567 → "1.2M"
// 45678 → "45.7K"
// 999 → "999"
```

### Currency Formatting
```typescript
function formatCurrency(value: number, currency = 'USD'): string {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
    notation: value > 1e6 ? 'compact' : 'standard'
  });

  return formatter.format(value);
}

// Examples:
// 1234567 → "$1.2M"
// 45678 → "$45,678"
// 999.99 → "$1,000"
```

### Percentage Formatting
```typescript
function formatPercentage(value: number, decimals = 1): string {
  const formatted = value.toFixed(decimals);
  const sign = value > 0 ? '+' : '';
  return `${sign}${formatted}%`;
}

// Examples:
// 15.345 → "+15.3%"
// -2.1 → "-2.1%"
// 0 → "0.0%"
```

## Trend Indicators

### Direction Arrows
```tsx
function TrendArrow({ direction, value }: TrendProps) {
  const arrows = {
    up: '↑',
    down: '↓',
    neutral: '→'
  };

  const colors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-500'
  };

  return (
    <span className={`flex items-center ${colors[direction]}`}>
      <span className="text-lg">{arrows[direction]}</span>
      <span className="ml-1">{formatPercentage(value)}</span>
    </span>
  );
}
```

### Status Badges
```tsx
function StatusBadge({ deltaType, value, label }: BadgeProps) {
  const styles = {
    increase: 'bg-green-100 text-green-800',
    decrease: 'bg-red-100 text-red-800',
    neutral: 'bg-gray-100 text-gray-800'
  };

  return (
    <div className={`inline-flex items-center px-2 py-1 rounded ${styles[deltaType]}`}>
      <TrendArrow direction={deltaType} />
      <span className="ml-1">{value}</span>
      {label && <span className="ml-2 text-sm">{label}</span>}
    </div>
  );
}
```

## Sparkline Integration

### Basic Sparkline
```tsx
import { Sparklines, SparklinesLine, SparklinesSpots } from 'react-sparklines';

function KPISparkline({ data, color = '#10b981' }) {
  return (
    <Sparklines data={data} width={100} height={30} margin={2}>
      <SparklinesLine
        style={{
          strokeWidth: 2,
          stroke: color,
          fill: 'none'
        }}
      />
      <SparklinesSpots
        size={2}
        style={{ fill: color }}
      />
    </Sparklines>
  );
}
```

### Inline SVG Sparkline (No Library)
```tsx
function MiniSparkline({ data, width = 100, height = 30 }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;

  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * width;
    const y = height - ((value - min) / range) * height;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg width={width} height={height} className="sparkline">
      <polyline
        points={points}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />
    </svg>
  );
}
```

## Card Variations

### Compact KPI Card
```tsx
function CompactKPI({ label, value, trend }) {
  return (
    <div className="flex items-center justify-between p-3">
      <div>
        <p className="text-xs text-gray-600">{label}</p>
        <p className="text-lg font-semibold">{value}</p>
      </div>
      {trend && (
        <div className="text-right">
          <TrendArrow {...trend} />
        </div>
      )}
    </div>
  );
}
```

### Detailed KPI Card
```tsx
function DetailedKPI({
  label,
  value,
  trend,
  sparkline,
  breakdown,
  actions
}) {
  return (
    <Card className="p-4">
      {/* Header */}
      <div className="flex justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-600">{label}</h3>
        <div className="flex gap-2">
          {actions?.map(action => (
            <IconButton key={action.id} {...action} />
          ))}
        </div>
      </div>

      {/* Main Value */}
      <div className="mb-3">
        <p className="text-3xl font-bold">{value}</p>
        {trend && <TrendIndicator {...trend} />}
      </div>

      {/* Sparkline */}
      {sparkline && (
        <div className="mb-3">
          <MiniSparkline data={sparkline} />
        </div>
      )}

      {/* Breakdown */}
      {breakdown && (
        <div className="border-t pt-3">
          {breakdown.map(item => (
            <div key={item.label} className="flex justify-between text-sm">
              <span className="text-gray-600">{item.label}</span>
              <span className="font-medium">{item.value}</span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
```

### Goal-Based KPI Card
```tsx
function GoalKPI({ label, current, target, unit = '' }) {
  const percentage = (current / target) * 100;
  const status = percentage >= 100 ? 'success' :
                  percentage >= 75 ? 'warning' : 'error';

  return (
    <Card className="p-4">
      <h3 className="text-sm text-gray-600 mb-2">{label}</h3>

      <div className="flex items-baseline gap-2 mb-3">
        <span className="text-2xl font-bold">
          {unit}{current.toLocaleString()}
        </span>
        <span className="text-sm text-gray-500">
          of {unit}{target.toLocaleString()}
        </span>
      </div>

      <ProgressBar value={percentage} status={status} />

      <p className="text-sm mt-2">
        {percentage.toFixed(1)}% of goal achieved
      </p>
    </Card>
  );
}
```

## Interactive Features

### Clickable KPI with Drill-Down
```tsx
function InteractiveKPI({ data, onDrillDown }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Card
      className="p-4 cursor-pointer transition-shadow"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={() => onDrillDown(data.id)}
      style={{
        boxShadow: isHovered ? 'var(--shadow-lg)' : 'var(--shadow-md)'
      }}
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-600">{data.label}</p>
          <p className="text-2xl font-bold mt-1">{data.value}</p>
        </div>
        {isHovered && (
          <ChevronRight className="text-gray-400" />
        )}
      </div>

      {data.trend && (
        <div className="mt-3">
          <TrendIndicator {...data.trend} />
        </div>
      )}
    </Card>
  );
}
```

### Real-Time Updating KPI
```tsx
function LiveKPI({ endpoint, label }) {
  const [data, setData] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource(endpoint);

    eventSource.onmessage = (event) => {
      setIsUpdating(true);
      const newData = JSON.parse(event.data);

      setTimeout(() => {
        setData(newData);
        setIsUpdating(false);
      }, 300);
    };

    return () => eventSource.close();
  }, [endpoint]);

  return (
    <Card className={`p-4 ${isUpdating ? 'animate-pulse' : ''}`}>
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-2xl font-bold mt-1">
        {data?.value || '---'}
      </p>
      {data?.lastUpdated && (
        <p className="text-xs text-gray-400 mt-2">
          Updated {formatRelativeTime(data.lastUpdated)}
        </p>
      )}
    </Card>
  );
}
```

## Accessibility

### ARIA Labels and Roles
```tsx
function AccessibleKPI({ label, value, trend }) {
  const trendDescription = trend
    ? `${trend.direction} ${trend.value}% ${trend.comparison}`
    : '';

  return (
    <div
      role="region"
      aria-label={`${label} metric`}
      className="kpi-card"
    >
      <h3 id={`kpi-${label}-title`}>{label}</h3>

      <div
        aria-labelledby={`kpi-${label}-title`}
        aria-describedby={`kpi-${label}-trend`}
      >
        <span className="sr-only">Current value:</span>
        <span className="text-2xl font-bold">{value}</span>
      </div>

      {trend && (
        <div id={`kpi-${label}-trend`}>
          <span className="sr-only">Trend:</span>
          <span aria-label={trendDescription}>
            <TrendArrow {...trend} />
          </span>
        </div>
      )}
    </div>
  );
}
```

### Keyboard Navigation
```tsx
function KeyboardNavigableKPI({ data, onSelect }) {
  return (
    <div
      tabIndex={0}
      role="button"
      aria-pressed={false}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onSelect(data);
        }
      }}
      onClick={() => onSelect(data)}
      className="kpi-card focus:ring-2 focus:ring-blue-500"
    >
      {/* KPI content */}
    </div>
  );
}
```

## Complete KPI Card Implementation

```tsx
function KPICard({
  label,
  value,
  unit = '',
  trend,
  sparkline,
  status = 'neutral',
  icon,
  onClick,
  className = ''
}) {
  const formattedValue = typeof value === 'number'
    ? formatLargeNumber(value)
    : value;

  const statusColors = {
    success: 'border-l-4 border-green-500',
    warning: 'border-l-4 border-yellow-500',
    error: 'border-l-4 border-red-500',
    neutral: ''
  };

  return (
    <Card
      className={`p-4 ${statusColors[status]} ${onClick ? 'cursor-pointer' : ''} ${className}`}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {icon && <span className="text-gray-500">{icon}</span>}
          <h3 className="text-sm font-medium text-gray-600">{label}</h3>
        </div>
      </div>

      {/* Value */}
      <div className="mb-3">
        <p className="text-2xl font-bold">
          {unit && <span className="text-lg">{unit}</span>}
          {formattedValue}
        </p>
      </div>

      {/* Trend */}
      {trend && (
        <div className="flex items-center gap-2 mb-3">
          <TrendArrow direction={trend.direction} />
          <span className="text-sm font-medium">
            {formatPercentage(trend.value)}
          </span>
          <span className="text-sm text-gray-500">
            {trend.comparison}
          </span>
        </div>
      )}

      {/* Sparkline */}
      {sparkline && sparkline.length > 0 && (
        <div className="mt-3">
          <MiniSparkline data={sparkline} />
        </div>
      )}
    </Card>
  );
}
```