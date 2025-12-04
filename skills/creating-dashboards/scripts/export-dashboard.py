#!/usr/bin/env python3
"""
Export Dashboard Data

Export dashboard data to CSV, JSON, or Excel for offline analysis or reporting.

Usage:
    python scripts/export-dashboard.py --format csv --output report.csv
    python scripts/export-dashboard.py --format excel --output report.xlsx --include-charts
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def generate_sample_data():
    """Generate sample dashboard data"""
    data = {
        "kpis": {
            "revenue": 63000,
            "users": 12543,
            "conversion_rate": 3.8,
            "growth_rate": 18.2,
        },
        "timeseries": [
            {"date": "2025-07-01", "revenue": 42000, "users": 9800},
            {"date": "2025-08-01", "revenue": 45000, "users": 10200},
            {"date": "2025-09-01", "revenue": 51000, "users": 11100},
            {"date": "2025-10-01", "revenue": 49000, "users": 10800},
            {"date": "2025-11-01", "revenue": 58000, "users": 12000},
            {"date": "2025-12-01", "revenue": 63000, "users": 12543},
        ],
        "products": [
            {"product": "Pro Plan", "sales": 125000, "units": 450},
            {"product": "Enterprise", "sales": 98000, "units": 120},
            {"product": "Starter", "sales": 67000, "units": 890},
            {"product": "Add-ons", "sales": 34000, "units": 1200},
        ],
        "regions": [
            {"region": "North America", "revenue": 280000, "users": 5200},
            {"region": "Europe", "revenue": 180000, "users": 3800},
            {"region": "Asia Pacific", "revenue": 120000, "users": 3543},
        ],
    }
    return data

def export_to_csv(data, output_path):
    """Export to CSV format"""
    import csv

    with open(output_path, 'w', newline='') as f:
        # Write KPIs section
        writer = csv.writer(f)
        writer.writerow(["Dashboard Export", datetime.now().isoformat()])
        writer.writerow([])
        writer.writerow(["KPIs"])
        writer.writerow(["Metric", "Value"])

        for key, value in data["kpis"].items():
            writer.writerow([key.replace('_', ' ').title(), value])

        writer.writerow([])
        writer.writerow(["Timeseries Data"])
        if data["timeseries"]:
            headers = list(data["timeseries"][0].keys())
            writer.writerow(headers)
            for row in data["timeseries"]:
                writer.writerow([row[h] for h in headers])

        writer.writerow([])
        writer.writerow(["Product Data"])
        if data["products"]:
            headers = list(data["products"][0].keys())
            writer.writerow(headers)
            for row in data["products"]:
                writer.writerow([row[h] for h in headers])

    print(f"✓ Exported to CSV: {output_path}")

def export_to_json(data, output_path):
    """Export to JSON format"""
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "dashboard_data": data,
    }

    with open(output_path, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"✓ Exported to JSON: {output_path}")

def export_to_excel(data, output_path, include_charts=False):
    """Export to Excel with multiple sheets"""
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas required for Excel export")
        print("Install: pip install pandas openpyxl")
        sys.exit(1)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # KPIs sheet
        kpi_df = pd.DataFrame([
            {"Metric": k.replace('_', ' ').title(), "Value": v}
            for k, v in data["kpis"].items()
        ])
        kpi_df.to_excel(writer, sheet_name='KPIs', index=False)

        # Timeseries sheet
        ts_df = pd.DataFrame(data["timeseries"])
        ts_df.to_excel(writer, sheet_name='Timeseries', index=False)

        # Products sheet
        prod_df = pd.DataFrame(data["products"])
        prod_df.to_excel(writer, sheet_name='Products', index=False)

        # Regions sheet
        region_df = pd.DataFrame(data["regions"])
        region_df.to_excel(writer, sheet_name='Regions', index=False)

        if include_charts:
            # Add charts to Excel (requires openpyxl)
            from openpyxl.chart import LineChart, Reference

            workbook = writer.book
            ts_sheet = workbook['Timeseries']

            # Create revenue trend chart
            chart = LineChart()
            chart.title = "Revenue Trend"
            chart.x_axis.title = "Date"
            chart.y_axis.title = "Revenue ($)"

            data_ref = Reference(ts_sheet, min_col=2, min_row=1, max_row=len(data["timeseries"]) + 1)
            cats_ref = Reference(ts_sheet, min_col=1, min_row=2, max_row=len(data["timeseries"]) + 1)

            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(cats_ref)

            ts_sheet.add_chart(chart, "E2")

    print(f"✓ Exported to Excel: {output_path}")
    if include_charts:
        print("  (with embedded charts)")

def main():
    parser = argparse.ArgumentParser(description="Export dashboard data")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "excel"],
        default="json",
        help="Export format"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--include-charts",
        action="store_true",
        help="Include charts in Excel export"
    )
    parser.add_argument(
        "--api-url",
        help="Fetch live data from API endpoint"
    )

    args = parser.parse_args()

    # Generate or fetch data
    if args.api_url:
        import requests
        try:
            response = requests.get(args.api_url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error fetching data from API: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Using sample data (use --api-url to fetch live data)")
        data = generate_sample_data()

    # Export based on format
    try:
        if args.format == "csv":
            export_to_csv(data, args.output)
        elif args.format == "json":
            export_to_json(data, args.output)
        elif args.format == "excel":
            export_to_excel(data, args.output, args.include_charts)

        print(f"\n✓ Export complete!")
        print(f"  Format: {args.format.upper()}")
        print(f"  File: {args.output}")

    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
