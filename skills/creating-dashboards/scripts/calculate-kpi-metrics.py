#!/usr/bin/env python3
"""
KPI Metrics Calculator
Calculates KPI values, trends, comparisons, and sparkline data from raw metrics.
"""

import json
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics


class KPICalculator:
    """Calculate KPI metrics including trends, comparisons, and sparklines."""

    def __init__(self):
        self.comparison_periods = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': timedelta(days=30),
            'quarterly': timedelta(days=90),
            'yearly': timedelta(days=365)
        }

    def calculate_kpi(self, data: List[Dict], config: Dict) -> Dict:
        """
        Calculate KPI metrics from raw data.

        Args:
            data: List of data points with timestamps and values
            config: Configuration for KPI calculation

        Returns:
            Dictionary with calculated KPI metrics
        """
        if not data:
            return self._empty_kpi()

        metric_field = config.get('metric', 'value')
        period = config.get('period', 'monthly')
        comparison = config.get('comparison', 'previous')

        # Extract values
        values = [d.get(metric_field, 0) for d in data]
        timestamps = [self._parse_timestamp(d.get('timestamp')) for d in data if d.get('timestamp')]

        # Calculate primary metric
        current_value = self._calculate_aggregate(values, config.get('aggregation', 'sum'))

        # Calculate trend
        trend = self._calculate_trend(values, timestamps, comparison)

        # Generate sparkline data
        sparkline = self._generate_sparkline(values, config.get('sparkline_points', 20))

        # Format the result
        result = {
            'value': current_value,
            'formatted_value': self._format_value(current_value, config.get('format', 'number')),
            'trend': trend,
            'sparkline': sparkline,
            'period': period,
            'last_updated': datetime.now().isoformat(),
            'data_points': len(values)
        }

        # Add additional metrics if configured
        if config.get('include_stats', False):
            result['statistics'] = self._calculate_statistics(values)

        if config.get('include_forecast', False):
            result['forecast'] = self._calculate_forecast(values, timestamps)

        return result

    def _calculate_aggregate(self, values: List[float], aggregation: str) -> float:
        """Calculate aggregate value based on aggregation type."""
        if not values:
            return 0.0

        aggregations = {
            'sum': sum(values),
            'average': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'count': len(values),
            'last': values[-1] if values else 0
        }

        return round(aggregations.get(aggregation, sum(values)), 2)

    def _calculate_trend(self, values: List[float], timestamps: List[datetime], comparison: str) -> Dict:
        """Calculate trend by comparing current to previous period."""
        if len(values) < 2:
            return {
                'direction': 'neutral',
                'value': 0,
                'percentage': 0,
                'comparison': comparison
            }

        # Split data into current and previous periods
        mid_point = len(values) // 2
        current_values = values[mid_point:]
        previous_values = values[:mid_point]

        current_sum = sum(current_values)
        previous_sum = sum(previous_values)

        if previous_sum == 0:
            percentage_change = 100 if current_sum > 0 else 0
        else:
            percentage_change = ((current_sum - previous_sum) / previous_sum) * 100

        absolute_change = current_sum - previous_sum

        return {
            'direction': 'up' if absolute_change > 0 else 'down' if absolute_change < 0 else 'neutral',
            'value': round(absolute_change, 2),
            'percentage': round(percentage_change, 1),
            'comparison': comparison,
            'current_period_value': round(current_sum, 2),
            'previous_period_value': round(previous_sum, 2)
        }

    def _generate_sparkline(self, values: List[float], points: int) -> List[float]:
        """Generate sparkline data points."""
        if not values:
            return []

        if len(values) <= points:
            return values

        # Sample evenly from the values
        step = len(values) / points
        sparkline = []

        for i in range(points):
            index = int(i * step)
            sparkline.append(round(values[index], 2))

        return sparkline

    def _calculate_statistics(self, values: List[float]) -> Dict:
        """Calculate statistical metrics for the values."""
        if not values:
            return {}

        return {
            'mean': round(statistics.mean(values), 2),
            'median': round(statistics.median(values), 2),
            'std_dev': round(statistics.stdev(values), 2) if len(values) > 1 else 0,
            'min': round(min(values), 2),
            'max': round(max(values), 2),
            'percentiles': {
                '25': round(statistics.quantiles(values, n=4)[0], 2) if len(values) > 1 else 0,
                '50': round(statistics.median(values), 2),
                '75': round(statistics.quantiles(values, n=4)[2], 2) if len(values) > 1 else 0
            }
        }

    def _calculate_forecast(self, values: List[float], timestamps: List[datetime]) -> Dict:
        """Calculate simple forecast based on trend."""
        if len(values) < 3:
            return {'next_period': None, 'confidence': 'low'}

        # Simple linear regression for trend
        n = len(values)
        x = list(range(n))

        mean_x = sum(x) / n
        mean_y = sum(values) / n

        numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator

        intercept = mean_y - slope * mean_x

        # Predict next value
        next_value = slope * n + intercept

        # Calculate confidence based on variance
        variance = statistics.variance(values) if len(values) > 1 else 0
        confidence = 'high' if variance < mean_y * 0.1 else 'medium' if variance < mean_y * 0.3 else 'low'

        return {
            'next_period': round(next_value, 2),
            'trend_slope': round(slope, 2),
            'confidence': confidence
        }

    def _format_value(self, value: float, format_type: str) -> str:
        """Format value based on type."""
        formatters = {
            'number': lambda v: f'{v:,.0f}',
            'decimal': lambda v: f'{v:,.2f}',
            'currency': lambda v: f'${v:,.2f}',
            'percentage': lambda v: f'{v:.1f}%',
            'compact': self._format_compact
        }

        formatter = formatters.get(format_type, formatters['number'])
        return formatter(value)

    def _format_compact(self, value: float) -> str:
        """Format large numbers in compact form (K, M, B)."""
        if abs(value) >= 1e9:
            return f'{value/1e9:.1f}B'
        elif abs(value) >= 1e6:
            return f'{value/1e6:.1f}M'
        elif abs(value) >= 1e3:
            return f'{value/1e3:.1f}K'
        else:
            return f'{value:.0f}'

    def _parse_timestamp(self, timestamp: Any) -> datetime:
        """Parse timestamp from various formats."""
        if isinstance(timestamp, datetime):
            return timestamp
        elif isinstance(timestamp, str):
            return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        else:
            return datetime.now()

    def _empty_kpi(self) -> Dict:
        """Return empty KPI structure."""
        return {
            'value': 0,
            'formatted_value': '0',
            'trend': {
                'direction': 'neutral',
                'value': 0,
                'percentage': 0
            },
            'sparkline': [],
            'last_updated': datetime.now().isoformat()
        }


def calculate_multiple_kpis(data: Dict[str, List[Dict]], configs: Dict[str, Dict]) -> Dict[str, Dict]:
    """Calculate multiple KPIs from different data sources."""
    calculator = KPICalculator()
    results = {}

    for kpi_id, config in configs.items():
        data_source = config.get('data_source', kpi_id)
        kpi_data = data.get(data_source, [])
        results[kpi_id] = calculator.calculate_kpi(kpi_data, config)

    return results


def generate_sample_data(days: int = 30) -> List[Dict]:
    """Generate sample data for testing."""
    import random
    from datetime import datetime, timedelta

    data = []
    base_value = 1000
    now = datetime.now()

    for i in range(days):
        timestamp = now - timedelta(days=days-i)
        # Add some randomness with trend
        value = base_value + (i * 10) + random.uniform(-50, 50)

        data.append({
            'timestamp': timestamp.isoformat(),
            'value': round(value, 2),
            'transactions': random.randint(50, 200),
            'users': random.randint(100, 500)
        })

    return data


def main():
    """Main function to run the KPI calculator."""
    parser = argparse.ArgumentParser(description='Calculate KPI metrics')
    parser.add_argument('--data', type=str, help='Path to data JSON file')
    parser.add_argument('--config', type=str, help='Path to KPI configuration JSON file')
    parser.add_argument('--metric', type=str, default='value', help='Metric field to calculate')
    parser.add_argument('--period', type=str, default='monthly', help='Period for comparison')
    parser.add_argument('--format', type=str, default='number', help='Value format type')
    parser.add_argument('--sample', action='store_true', help='Use sample data')
    parser.add_argument('--output', type=str, help='Output file path')

    args = parser.parse_args()

    calculator = KPICalculator()

    # Load or generate data
    if args.sample:
        data = generate_sample_data(30)
        print("Generated 30 days of sample data")
    elif args.data:
        with open(args.data, 'r') as f:
            data = json.load(f)
    else:
        print("Error: Please provide --data file or use --sample")
        return

    # Load or create config
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        config = {
            'metric': args.metric,
            'period': args.period,
            'format': args.format,
            'aggregation': 'sum',
            'comparison': 'previous',
            'sparkline_points': 20,
            'include_stats': True,
            'include_forecast': True
        }

    # Calculate KPI
    result = calculator.calculate_kpi(data, config)

    # Display results
    print("\nKPI Metrics Calculated:")
    print(f"  Value: {result['formatted_value']}")
    print(f"  Trend: {result['trend']['direction']} ({result['trend']['percentage']}%)")
    print(f"  Data Points: {result.get('data_points', 0)}")

    if 'statistics' in result:
        print(f"\nStatistics:")
        for key, value in result['statistics'].items():
            if key != 'percentiles':
                print(f"  {key}: {value}")

    if 'forecast' in result:
        print(f"\nForecast:")
        print(f"  Next Period: {result['forecast']['next_period']}")
        print(f"  Confidence: {result['forecast']['confidence']}")

    # Save output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")
    else:
        print(f"\nSparkline: {result['sparkline'][:10]}..." if len(result['sparkline']) > 10 else f"\nSparkline: {result['sparkline']}")


if __name__ == '__main__':
    main()