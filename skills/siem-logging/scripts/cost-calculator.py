#!/usr/bin/env python3
"""
SIEM Cost Calculator

Estimates SIEM costs based on log volume, retention period, and storage tiering strategy.
"""

import argparse
from decimal import Decimal


def calculate_costs(daily_gb, retention_days, hot_days=30, warm_days=90):
    """
    Calculate SIEM storage costs with hot/warm/cold tiering.

    Args:
        daily_gb: Daily log volume in GB
        retention_days: Total retention period in days
        hot_days: Days to keep in hot tier (default: 30)
        warm_days: Days to keep in warm tier (default: 90)

    Returns:
        Dictionary with cost breakdown
    """
    # Storage costs per GB/month
    hot_cost = Decimal('0.10')   # SSD, high-IOPS
    warm_cost = Decimal('0.05')  # HDD, lower IOPS
    cold_cost = Decimal('0.01')  # S3 Glacier, archival

    daily_gb = Decimal(str(daily_gb))

    # Calculate total data per tier
    hot_total_gb = daily_gb * min(hot_days, retention_days)
    warm_total_gb = daily_gb * max(0, min(warm_days, retention_days - hot_days))
    cold_total_gb = daily_gb * max(0, retention_days - hot_days - warm_days)

    # Convert to TB for readability
    hot_tb = hot_total_gb / 1000
    warm_tb = warm_total_gb / 1000
    cold_tb = cold_total_gb / 1000

    # Calculate monthly costs
    hot_monthly = (hot_total_gb * hot_cost).quantize(Decimal('0.01'))
    warm_monthly = (warm_total_gb * warm_cost).quantize(Decimal('0.01'))
    cold_monthly = (cold_total_gb * cold_cost).quantize(Decimal('0.01'))

    total_monthly = hot_monthly + warm_monthly + cold_monthly
    total_annual = total_monthly * 12

    # Calculate hot-only costs for comparison
    total_gb = daily_gb * retention_days
    hot_only_monthly = (total_gb * hot_cost).quantize(Decimal('0.01'))
    hot_only_annual = hot_only_monthly * 12

    savings_monthly = hot_only_monthly - total_monthly
    savings_annual = hot_only_annual - total_annual
    savings_percent = ((savings_annual / hot_only_annual) * 100).quantize(Decimal('0.1'))

    return {
        'hot': {
            'days': hot_days,
            'tb': float(hot_tb),
            'monthly': float(hot_monthly),
            'annual': float(hot_monthly * 12)
        },
        'warm': {
            'days': warm_days - hot_days if warm_days > hot_days else 0,
            'tb': float(warm_tb),
            'monthly': float(warm_monthly),
            'annual': float(warm_monthly * 12)
        },
        'cold': {
            'days': retention_days - warm_days if retention_days > warm_days else 0,
            'tb': float(cold_tb),
            'monthly': float(cold_monthly),
            'annual': float(cold_monthly * 12)
        },
        'total': {
            'monthly': float(total_monthly),
            'annual': float(total_annual)
        },
        'comparison': {
            'hot_only_monthly': float(hot_only_monthly),
            'hot_only_annual': float(hot_only_annual),
            'savings_monthly': float(savings_monthly),
            'savings_annual': float(savings_annual),
            'savings_percent': float(savings_percent)
        }
    }


def print_cost_report(costs, daily_gb, retention_days):
    """Print formatted cost report."""
    print("\n" + "="*60)
    print(f"SIEM Cost Estimation")
    print("="*60)
    print(f"\nInput Parameters:")
    print(f"  Daily Log Volume: {daily_gb} GB/day")
    print(f"  Total Retention: {retention_days} days")

    print(f"\nStorage Tiering Breakdown:")
    print(f"  Hot Tier ({costs['hot']['days']} days):")
    print(f"    Volume: {costs['hot']['tb']:.2f} TB")
    print(f"    Cost: ${costs['hot']['monthly']:,.2f}/month (${costs['hot']['annual']:,.2f}/year)")

    print(f"  Warm Tier ({costs['warm']['days']} days):")
    print(f"    Volume: {costs['warm']['tb']:.2f} TB")
    print(f"    Cost: ${costs['warm']['monthly']:,.2f}/month (${costs['warm']['annual']:,.2f}/year)")

    print(f"  Cold Tier ({costs['cold']['days']} days):")
    print(f"    Volume: {costs['cold']['tb']:.2f} TB")
    print(f"    Cost: ${costs['cold']['monthly']:,.2f}/month (${costs['cold']['annual']:,.2f}/year)")

    print(f"\nTotal Cost:")
    print(f"  Monthly: ${costs['total']['monthly']:,.2f}")
    print(f"  Annual: ${costs['total']['annual']:,.2f}")

    print(f"\nComparison (Hot-Only Storage):")
    print(f"  Hot-Only Monthly: ${costs['comparison']['hot_only_monthly']:,.2f}")
    print(f"  Hot-Only Annual: ${costs['comparison']['hot_only_annual']:,.2f}")
    print(f"  Savings: ${costs['comparison']['savings_annual']:,.2f}/year ({costs['comparison']['savings_percent']:.1f}%)")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Calculate SIEM storage costs with tiering strategy'
    )
    parser.add_argument(
        '--daily-gb',
        type=float,
        required=True,
        help='Daily log volume in GB'
    )
    parser.add_argument(
        '--retention-days',
        type=int,
        required=True,
        help='Total retention period in days'
    )
    parser.add_argument(
        '--hot-days',
        type=int,
        default=30,
        help='Days to keep in hot tier (default: 30)'
    )
    parser.add_argument(
        '--warm-days',
        type=int,
        default=90,
        help='Total days in hot+warm tier (default: 90)'
    )

    args = parser.parse_args()

    costs = calculate_costs(
        args.daily_gb,
        args.retention_days,
        args.hot_days,
        args.warm_days
    )

    print_cost_report(costs, args.daily_gb, args.retention_days)


if __name__ == '__main__':
    main()
