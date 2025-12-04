#!/usr/bin/env python3
"""
Dashboard Performance Optimizer

Analyzes dashboard configuration and provides optimization recommendations.

Usage:
    python scripts/optimize-dashboard-performance.py --config dashboard.json
    python scripts/optimize-dashboard-performance.py --widgets 12 --auto-refresh-count 8
"""

import argparse
import json
import sys
from typing import Dict, List, Any


def analyze_widget_count(num_widgets: int) -> List[str]:
    """Analyze widget count and provide recommendations"""
    recommendations = []

    if num_widgets > 20:
        recommendations.append({
            "severity": "high",
            "issue": f"Too many widgets ({num_widgets})",
            "recommendation": "Reduce to <20 widgets or use pagination/tabs",
            "impact": "Slow initial render, high memory usage"
        })
    elif num_widgets > 12:
        recommendations.append({
            "severity": "medium",
            "issue": f"Many widgets ({num_widgets})",
            "recommendation": "Consider splitting into multiple dashboard pages",
            "impact": "Moderate performance impact"
        })

    return recommendations


def analyze_refresh_rates(widgets: List[Dict]) -> List[str]:
    """Analyze refresh rates and auto-polling"""
    recommendations = []

    auto_refresh_widgets = [w for w in widgets if w.get('autoRefresh', False)]

    if len(auto_refresh_widgets) > 10:
        recommendations.append({
            "severity": "high",
            "issue": f"{len(auto_refresh_widgets)} widgets with auto-refresh",
            "recommendation": "Reduce auto-refreshing widgets to <10. Use manual refresh or SSE.",
            "impact": "High backend load, network congestion"
        })

    # Check refresh intervals
    fast_refresh = [w for w in auto_refresh_widgets if w.get('refreshInterval', 30000) < 5000]
    if fast_refresh:
        recommendations.append({
            "severity": "high",
            "issue": f"{len(fast_refresh)} widgets refreshing <5 seconds",
            "recommendation": "Increase refresh interval to >=5 seconds or use WebSocket/SSE",
            "impact": "Excessive API calls, poor UX"
        })

    return recommendations


def analyze_data_fetching(widgets: List[Dict]) -> List[str]:
    """Analyze data fetching patterns"""
    recommendations = []

    # Check for N+1 queries
    individual_fetches = [w for w in widgets if w.get('fetchMode') == 'individual']

    if len(individual_fetches) > 5:
        recommendations.append({
            "severity": "medium",
            "issue": f"{len(individual_fetches)} widgets with individual data fetching",
            "recommendation": "Batch data fetching - single API call for all dashboard data",
            "impact": "Multiple sequential API calls slow initial load"
        })

    # Check for heavy queries
    heavy_widgets = [w for w in widgets if w.get('dataSize', 0) > 10000]
    if heavy_widgets:
        recommendations.append({
            "severity": "medium",
            "issue": f"{len(heavy_widgets)} widgets fetching large datasets (>10K rows)",
            "recommendation": "Implement server-side pagination, aggregation, or caching",
            "impact": "Large payload sizes, slow rendering"
        })

    return recommendations


def analyze_chart_complexity(widgets: List[Dict]) -> List[str]:
    """Analyze chart rendering complexity"""
    recommendations = []

    chart_widgets = [w for w in widgets if w.get('type', '').endswith('chart')]
    large_charts = [w for w in chart_widgets if w.get('dataPoints', 0) > 1000]

    if large_charts:
        recommendations.append({
            "severity": "medium",
            "issue": f"{len(large_charts)} charts with >1000 data points",
            "recommendation": "Downsample data (LTTB algorithm) or use virtualization",
            "impact": "Slow chart rendering, laggy interactions"
        })

    return recommendations


def generate_recommendations(config: Dict[str, Any]) -> List[Dict]:
    """Generate all recommendations"""
    all_recommendations = []

    widgets = config.get('widgets', [])
    num_widgets = len(widgets)

    all_recommendations.extend(analyze_widget_count(num_widgets))
    all_recommendations.extend(analyze_refresh_rates(widgets))
    all_recommendations.extend(analyze_data_fetching(widgets))
    all_recommendations.extend(analyze_chart_complexity(widgets))

    return all_recommendations


def print_recommendations(recommendations: List[Dict]):
    """Print recommendations to console"""
    if not recommendations:
        print("✓ No performance issues detected!")
        return

    print("Dashboard Performance Analysis")
    print("=" * 70)

    # Group by severity
    high = [r for r in recommendations if r['severity'] == 'high']
    medium = [r for r in recommendations if r['severity'] == 'medium']
    low = [r for r in recommendations if r['severity'] == 'low']

    if high:
        print(f"\n🔴 HIGH PRIORITY ({len(high)} issues)")
        print("-" * 70)
        for rec in high:
            print(f"\nIssue: {rec['issue']}")
            print(f"  ➜ {rec['recommendation']}")
            print(f"  Impact: {rec['impact']}")

    if medium:
        print(f"\n🟡 MEDIUM PRIORITY ({len(medium)} issues)")
        print("-" * 70)
        for rec in medium:
            print(f"\nIssue: {rec['issue']}")
            print(f"  ➜ {rec['recommendation']}")
            print(f"  Impact: {rec['impact']}")

    if low:
        print(f"\n🟢 LOW PRIORITY ({len(low)} issues)")
        print("-" * 70)
        for rec in low:
            print(f"\nIssue: {rec['issue']}")
            print(f"  ➜ {rec['recommendation']}")


def main():
    parser = argparse.ArgumentParser(description="Optimize dashboard performance")
    parser.add_argument(
        "--config",
        help="Path to dashboard configuration JSON"
    )
    parser.add_argument(
        "--widgets",
        type=int,
        help="Number of widgets (if not using config file)"
    )
    parser.add_argument(
        "--auto-refresh-count",
        type=int,
        help="Number of auto-refreshing widgets"
    )

    args = parser.parse_args()

    if args.config:
        if not Path(args.config).exists():
            print(f"Error: Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)

        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        # Build config from CLI args
        config = {
            "widgets": [
                {"id": f"widget-{i}", "autoRefresh": i < (args.auto_refresh_count or 0)}
                for i in range(args.widgets or 0)
            ]
        }

    # Generate recommendations
    recommendations = generate_recommendations(config)

    # Print results
    print_recommendations(recommendations)

    # Exit with error if high-priority issues found
    high_priority = [r for r in recommendations if r['severity'] == 'high']
    if high_priority:
        print(f"\n⚠ {len(high_priority)} high-priority performance issues found")
        sys.exit(1)
    else:
        print("\n✓ Dashboard performance is acceptable")
        sys.exit(0)


if __name__ == "__main__":
    main()
