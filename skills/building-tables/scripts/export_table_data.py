#!/usr/bin/env python3
"""
Export Table Data

Export table data to CSV, JSON, or Excel formats.

Usage:
    python scripts/export_table_data.py --format csv --output data.csv
    python scripts/export_table_data.py --format excel --output report.xlsx
    python scripts/export_table_data.py --api-url http://localhost:3000/api/users --format json
"""

import argparse
import json
import sys
from typing import List, Dict, Any

def generate_sample_data() -> List[Dict[str, Any]]:
    """Generate sample table data"""
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "Admin", "status": "active"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "User", "status": "active"},
        {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "role": "User", "status": "inactive"},
    ]

def export_to_csv(data: List[Dict], output_path: str):
    """Export to CSV"""
    import csv

    if not data:
        print("No data to export", file=sys.stderr)
        return

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✓ Exported {len(data)} rows to CSV: {output_path}")

def export_to_json(data: List[Dict], output_path: str):
    """Export to JSON"""
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Exported {len(data)} rows to JSON: {output_path}")

def export_to_excel(data: List[Dict], output_path: str):
    """Export to Excel"""
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas required for Excel export")
        print("Install: pip install pandas openpyxl")
        sys.exit(1)

    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False, sheet_name='Data')

    print(f"✓ Exported {len(data)} rows to Excel: {output_path}")

def fetch_from_api(url: str) -> List[Dict]:
    """Fetch data from API"""
    import requests

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching from API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Export table data")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "excel"],
        required=True,
        help="Export format"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--api-url",
        help="Fetch data from API endpoint (optional)"
    )

    args = parser.parse_args()

    # Get data
    if args.api_url:
        print(f"Fetching data from: {args.api_url}")
        data = fetch_from_api(args.api_url)
    else:
        print("Using sample data")
        data = generate_sample_data()

    # Export
    if args.format == "csv":
        export_to_csv(data, args.output)
    elif args.format == "json":
        export_to_json(data, args.output)
    elif args.format == "excel":
        export_to_excel(data, args.output)

if __name__ == "__main__":
    main()
