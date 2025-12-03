#!/usr/bin/env python3
"""
Generate Retention Policy Recommendations

Analyzes data volume and query patterns to recommend optimal retention policies.

Usage:
    python generate_retention_policy.py --table metrics --daily-rows 1000000
"""

import argparse
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class RetentionRecommendation:
    """Retention policy recommendation."""

    data_type: str
    retention_days: int
    storage_gb: float
    reasoning: str


def calculate_storage(daily_rows: int, row_size_bytes: int, days: int) -> float:
    """Calculate storage in GB."""
    total_bytes = daily_rows * row_size_bytes * days
    return total_bytes / (1024**3)  # Convert to GB


def generate_recommendations(
    daily_rows: int,
    row_size_bytes: int = 100,
    use_case: str = "general",
    budget_gb: int = 1000,
) -> List[RetentionRecommendation]:
    """
    Generate retention policy recommendations.

    Args:
        daily_rows: Number of rows inserted per day
        row_size_bytes: Average row size in bytes
        use_case: Use case type (general, devops, iot, financial, analytics)
        budget_gb: Storage budget in GB

    Returns:
        List of retention recommendations
    """
    recommendations = []

    # Use case templates
    templates = {
        "general": {
            "raw": 30,
            "1min": 90,
            "1hour": 365,
            "daily": None,  # Forever
        },
        "devops": {
            "raw": 7,
            "1min": 30,
            "1hour": 365,
            "daily": None,
        },
        "iot": {
            "raw": 30,
            "1min": 90,
            "1hour": 730,  # 2 years
            "daily": None,
        },
        "financial": {
            "raw": 90,  # Compliance
            "1min": 365,
            "1hour": 2555,  # 7 years
            "daily": None,
        },
        "analytics": {
            "raw": 7,
            "1min": 30,
            "1hour": 365,
            "daily": None,
        },
    }

    template = templates.get(use_case, templates["general"])

    # Raw data
    raw_days = template["raw"]
    raw_storage = calculate_storage(daily_rows, row_size_bytes, raw_days)
    recommendations.append(
        RetentionRecommendation(
            data_type="Raw Data",
            retention_days=raw_days,
            storage_gb=raw_storage,
            reasoning=f"High-resolution data for recent troubleshooting and analysis",
        )
    )

    # 1-minute rollup
    oneminute_days = template["1min"]
    # 1-minute rollup: 1440 points/day (one per minute) vs. raw points
    rollup_reduction_1min = daily_rows / 1440
    oneminute_row_size = row_size_bytes * 1.5  # Slightly larger (stores AVG, MAX, MIN)
    oneminute_storage = calculate_storage(
        int(1440), int(oneminute_row_size), oneminute_days
    )
    recommendations.append(
        RetentionRecommendation(
            data_type="1-Minute Rollup",
            retention_days=oneminute_days,
            storage_gb=oneminute_storage,
            reasoning=f"Medium-resolution for short-term analysis ({rollup_reduction_1min:.0f}x reduction)",
        )
    )

    # 1-hour rollup
    onehour_days = template["1hour"]
    # 1-hour rollup: 24 points/day
    rollup_reduction_1hour = daily_rows / 24
    onehour_row_size = row_size_bytes * 2  # Larger (stores AVG, MAX, MIN, STDDEV)
    onehour_storage = calculate_storage(24, int(onehour_row_size), onehour_days)
    recommendations.append(
        RetentionRecommendation(
            data_type="1-Hour Rollup",
            retention_days=onehour_days,
            storage_gb=onehour_storage,
            reasoning=f"Long-term trends ({rollup_reduction_1hour:.0f}x reduction)",
        )
    )

    # Daily rollup
    daily_days = template["daily"]
    if daily_days is None:
        daily_days_str = "∞"
        # Calculate 10 years for storage estimate
        daily_storage = calculate_storage(1, int(onehour_row_size), 3650)
    else:
        daily_days_str = str(daily_days)
        daily_storage = calculate_storage(1, int(onehour_row_size), daily_days)

    rollup_reduction_daily = daily_rows / 1
    recommendations.append(
        RetentionRecommendation(
            data_type="Daily Rollup",
            retention_days=daily_days if daily_days else float("inf"),
            storage_gb=daily_storage,
            reasoning=f"Historical reporting ({rollup_reduction_daily:.0f}x reduction)",
        )
    )

    # Calculate total storage
    total_storage = sum(r.storage_gb for r in recommendations if r.retention_days)

    # Check budget
    if total_storage > budget_gb:
        print(f"\n⚠️  WARNING: Estimated storage ({total_storage:.2f} GB) exceeds budget ({budget_gb} GB)")
        print("Consider:")
        print("  - Reducing retention periods")
        print("  - Increasing compression")
        print("  - Sampling data (keep 1 in N points)")

    return recommendations


def generate_sql(
    table_name: str, recommendations: List[RetentionRecommendation]
) -> str:
    """Generate SQL statements for retention policies."""
    sql = f"-- Retention policies for {table_name}\n\n"

    for rec in recommendations:
        if rec.retention_days == float("inf"):
            sql += f"-- {rec.data_type}: Keep forever (no retention policy)\n"
        else:
            table_suffix = {
                "Raw Data": "",
                "1-Minute Rollup": "_1min",
                "1-Hour Rollup": "_1hour",
                "Daily Rollup": "_daily",
            }[rec.data_type]

            sql += f"-- {rec.data_type}: {rec.retention_days} days\n"
            sql += f"SELECT add_retention_policy('{table_name}{table_suffix}', INTERVAL '{rec.retention_days} days');\n\n"

    return sql


def print_table(recommendations: List[RetentionRecommendation]):
    """Print recommendations as a formatted table."""
    print("\n📋 Retention Policy Recommendations")
    print("=" * 80)
    print(
        f"{'Data Type':<20} {'Retention':<15} {'Storage (GB)':<15} {'Reasoning':<30}"
    )
    print("-" * 80)

    total_storage = 0
    for rec in recommendations:
        retention_str = (
            f"{rec.retention_days} days"
            if rec.retention_days != float("inf")
            else "Forever"
        )
        storage_str = f"{rec.storage_gb:.2f} GB"
        print(
            f"{rec.data_type:<20} {retention_str:<15} {storage_str:<15} {rec.reasoning:<30}"
        )
        if rec.retention_days != float("inf"):
            total_storage += rec.storage_gb

    print("-" * 80)
    print(f"{'TOTAL':<20} {'':<15} {total_storage:.2f} GB")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Generate retention policy recommendations"
    )
    parser.add_argument("--table", required=True, help="Table name")
    parser.add_argument(
        "--daily-rows", type=int, required=True, help="Rows inserted per day"
    )
    parser.add_argument(
        "--row-size", type=int, default=100, help="Average row size in bytes"
    )
    parser.add_argument(
        "--use-case",
        choices=["general", "devops", "iot", "financial", "analytics"],
        default="general",
        help="Use case type",
    )
    parser.add_argument(
        "--budget-gb", type=int, default=1000, help="Storage budget in GB"
    )
    parser.add_argument(
        "--output-sql", help="Write SQL statements to file (optional)"
    )

    args = parser.parse_args()

    # Generate recommendations
    recommendations = generate_recommendations(
        daily_rows=args.daily_rows,
        row_size_bytes=args.row_size,
        use_case=args.use_case,
        budget_gb=args.budget_gb,
    )

    # Print table
    print_table(recommendations)

    # Print use case description
    use_case_descriptions = {
        "general": "Balanced retention for general time-series data",
        "devops": "Short retention for high-volume DevOps metrics",
        "iot": "Medium retention for IoT sensor data",
        "financial": "Long retention for compliance (7-year requirement)",
        "analytics": "Short raw data, focus on rollups for analytics",
    }
    print(f"\n📝 Use Case: {args.use_case.upper()}")
    print(f"   {use_case_descriptions[args.use_case]}")

    # Print storage breakdown
    print("\n💾 Storage Breakdown:")
    print(f"   Daily ingestion: {args.daily_rows:,} rows/day")
    print(f"   Average row size: {args.row_size} bytes")
    print(
        f"   Daily data volume: {(args.daily_rows * args.row_size) / (1024**2):.2f} MB/day"
    )

    # Generate SQL
    sql = generate_sql(args.table, recommendations)

    if args.output_sql:
        with open(args.output_sql, "w") as f:
            f.write(sql)
        print(f"\n✅ SQL written to {args.output_sql}")
    else:
        print(f"\n📜 SQL Statements:\n")
        print(sql)


if __name__ == "__main__":
    main()
