#!/usr/bin/env python3
"""
Reserved Instance and Savings Plan Coverage Report

Analyzes RI/SP utilization and coverage to identify optimization opportunities.

Usage:
    python ri_coverage_report.py --days 30
    python ri_coverage_report.py --days 30 --json > report.json

Dependencies:
    pip install boto3 tabulate

Environment Variables:
    AWS_REGION (optional): AWS region (default: us-east-1)
"""

import boto3
import argparse
from datetime import datetime, timedelta
from typing import Dict, List
from tabulate import tabulate


class RICoverageAnalyzer:
    """Analyze Reserved Instance and Savings Plan coverage and utilization."""

    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ce = boto3.client('ce', region_name=region)  # Cost Explorer

    def get_ri_utilization(self, days: int = 30) -> Dict:
        """Get Reserved Instance utilization for past N days."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        response = self.ce.get_reservation_utilization(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY'
        )

        total = response['Total']
        utilization_pct = float(total['UtilizationPercentage'])
        purchased_hours = float(total['PurchasedHours'])
        used_hours = float(total['TotalActualHours'])
        unused_hours = float(total['UnusedHours'])

        # Calculate wasted cost
        unused_units = float(total.get('UnusedUnits', 0))
        wasted_cost = float(total.get('AmortizedUpfrontFee', 0)) + float(total.get('AmortizedRecurringFee', 0))
        wasted_cost *= (unused_hours / purchased_hours) if purchased_hours > 0 else 0

        return {
            'utilization_pct': utilization_pct,
            'purchased_hours': purchased_hours,
            'used_hours': used_hours,
            'unused_hours': unused_hours,
            'wasted_cost': wasted_cost,
            'target_utilization': 95.0,
            'meets_target': utilization_pct >= 95.0
        }

    def get_savings_plan_utilization(self, days: int = 30) -> Dict:
        """Get Savings Plan utilization for past N days."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        try:
            response = self.ce.get_savings_plans_utilization(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY'
            )

            total = response['Total']
            utilization_pct = float(total['Utilization']['UtilizationPercentage'])
            unused_commitment = float(total.get('UnusedCommitment', 0))

            return {
                'utilization_pct': utilization_pct,
                'unused_commitment': unused_commitment,
                'target_utilization': 95.0,
                'meets_target': utilization_pct >= 95.0
            }
        except Exception as e:
            # No Savings Plans found
            return {
                'utilization_pct': 0.0,
                'unused_commitment': 0.0,
                'target_utilization': 95.0,
                'meets_target': False,
                'error': str(e)
            }

    def get_ri_coverage(self, days: int = 30) -> Dict:
        """Get Reserved Instance coverage (what % of usage is covered by RIs)."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        response = self.ce.get_reservation_coverage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY'
        )

        total = response['Total']
        coverage_pct = float(total['CoverageHours']['CoverageHoursPercentage'])
        on_demand_hours = float(total['CoverageHours'].get('OnDemandHours', 0))
        reserved_hours = float(total['CoverageHours'].get('ReservedHours', 0))
        total_hours = float(total['CoverageHours'].get('TotalRunningHours', 0))

        # Calculate potential savings if all on-demand hours were reserved (40% discount)
        potential_savings = on_demand_hours * 0.40  # Rough estimate

        return {
            'coverage_pct': coverage_pct,
            'on_demand_hours': on_demand_hours,
            'reserved_hours': reserved_hours,
            'total_hours': total_hours,
            'potential_monthly_savings': potential_savings,
            'target_coverage': 70.0,
            'meets_target': coverage_pct >= 70.0
        }

    def get_savings_plan_coverage(self, days: int = 30) -> Dict:
        """Get Savings Plan coverage."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        try:
            response = self.ce.get_savings_plans_coverage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY'
            )

            if response['SavingsPlansCoverages']:
                total = response['SavingsPlansCoverages'][0]
                coverage_pct = float(total['Coverage']['CoveragePercentage'])
                on_demand_cost = float(total['Coverage'].get('OnDemandCost', 0))
                sp_covered_cost = float(total['Coverage'].get('SpendCoveredBySavingsPlans', 0))
                total_cost = float(total['Coverage'].get('TotalCost', 0))

                return {
                    'coverage_pct': coverage_pct,
                    'on_demand_cost': on_demand_cost,
                    'sp_covered_cost': sp_covered_cost,
                    'total_cost': total_cost,
                    'target_coverage': 70.0,
                    'meets_target': coverage_pct >= 70.0
                }
        except Exception:
            pass

        return {
            'coverage_pct': 0.0,
            'on_demand_cost': 0.0,
            'sp_covered_cost': 0.0,
            'total_cost': 0.0,
            'target_coverage': 70.0,
            'meets_target': False
        }

    def generate_report(self, days: int = 30) -> Dict:
        """Generate comprehensive RI/SP coverage and utilization report."""
        print("=" * 80)
        print(f"Reserved Instance & Savings Plan Report ({days} days)")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # RI Utilization
        ri_util = self.get_ri_utilization(days)
        print("\n📊 Reserved Instance Utilization")
        print(f"  Utilization: {ri_util['utilization_pct']:.2f}% " +
              f"({'✅ GOOD' if ri_util['meets_target'] else '❌ BELOW TARGET (95%)'})")
        print(f"  Purchased Hours: {ri_util['purchased_hours']:,.0f}")
        print(f"  Used Hours: {ri_util['used_hours']:,.0f}")
        print(f"  Unused Hours: {ri_util['unused_hours']:,.0f}")
        print(f"  Wasted Cost: ${ri_util['wasted_cost']:,.2f}")

        # RI Coverage
        ri_cov = self.get_ri_coverage(days)
        print("\n📈 Reserved Instance Coverage")
        print(f"  Coverage: {ri_cov['coverage_pct']:.2f}% " +
              f"({'✅ GOOD' if ri_cov['meets_target'] else '⚠️  BELOW TARGET (70%)'})")
        print(f"  On-Demand Hours: {ri_cov['on_demand_hours']:,.0f}")
        print(f"  Reserved Hours: {ri_cov['reserved_hours']:,.0f}")
        print(f"  💡 Potential Savings: ${ri_cov['potential_monthly_savings']:,.2f}/month")

        # Savings Plan Utilization
        sp_util = self.get_savings_plan_utilization(days)
        print("\n📊 Savings Plan Utilization")
        if 'error' in sp_util:
            print(f"  No Savings Plans found")
        else:
            print(f"  Utilization: {sp_util['utilization_pct']:.2f}% " +
                  f"({'✅ GOOD' if sp_util['meets_target'] else '❌ BELOW TARGET (95%)'})")
            print(f"  Unused Commitment: ${sp_util['unused_commitment']:,.2f}")

        # Savings Plan Coverage
        sp_cov = self.get_savings_plan_coverage(days)
        print("\n📈 Savings Plan Coverage")
        print(f"  Coverage: {sp_cov['coverage_pct']:.2f}% " +
              f"({'✅ GOOD' if sp_cov['meets_target'] else '⚠️  BELOW TARGET (70%)'})")
        print(f"  On-Demand Cost: ${sp_cov['on_demand_cost']:,.2f}")
        print(f"  SP Covered Cost: ${sp_cov['sp_covered_cost']:,.2f}")

        # Recommendations
        print("\n" + "=" * 80)
        print("💡 RECOMMENDATIONS")
        print("=" * 80)

        recommendations = []

        if not ri_util['meets_target']:
            recommendations.append(
                f"⚠️  RI utilization at {ri_util['utilization_pct']:.1f}% (target 95%). "
                "Consider selling unused RIs on marketplace or modifying instance types."
            )

        if not ri_cov['meets_target']:
            recommendations.append(
                f"⚠️  RI coverage at {ri_cov['coverage_pct']:.1f}% (target 70%). "
                f"Purchase more RIs to save ${ri_cov['potential_monthly_savings']:,.2f}/month."
            )

        if not sp_util.get('error') and not sp_util['meets_target']:
            recommendations.append(
                f"⚠️  SP utilization at {sp_util['utilization_pct']:.1f}% (target 95%). "
                "Review Savings Plan commitments and adjust."
            )

        if not sp_cov['meets_target'] and sp_cov['coverage_pct'] > 0:
            recommendations.append(
                f"⚠️  SP coverage at {sp_cov['coverage_pct']:.1f}% (target 70%). "
                "Consider purchasing additional Savings Plans."
            )

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        else:
            print("✅ All metrics meet targets. Great job!")

        return {
            'ri_utilization': ri_util,
            'ri_coverage': ri_cov,
            'sp_utilization': sp_util,
            'sp_coverage': sp_cov,
            'recommendations': recommendations
        }


def main():
    parser = argparse.ArgumentParser(description='Generate RI/SP coverage report')
    parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    analyzer = RICoverageAnalyzer(region=args.region)
    report = analyzer.generate_report(days=args.days)

    if args.json:
        import json
        print("\n" + json.dumps(report, indent=2, default=str))


if __name__ == '__main__':
    main()
