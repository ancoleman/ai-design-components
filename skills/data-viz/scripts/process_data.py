#!/usr/bin/env python3
"""
Process and transform data for visualization

Common transformations:
- CSV to JSON
- Aggregate/group data
- Calculate percentages
- Bin continuous data for histograms
- Downsample large datasets

Usage:
    python process_data.py sales.csv --to-json sales.json
    python process_data.py data.csv --aggregate category --metric sum
    python process_data.py large-data.csv --downsample 500
"""

import argparse
import csv
import json
from pathlib import Path
from typing import List, Dict, Any
import sys

def csv_to_json(csv_path: Path) -> List[Dict[str, Any]]:
    """Convert CSV to JSON array of objects"""
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def aggregate_data(data: List[Dict], group_by: str, value_field: str, operation: str = 'sum') -> List[Dict]:
    """Aggregate data by grouping field"""
    groups = {}

    for row in data:
        key = row[group_by]
        value = float(row[value_field])

        if key not in groups:
            groups[key] = []
        groups[key].append(value)

    result = []
    for key, values in groups.items():
        if operation == 'sum':
            agg_value = sum(values)
        elif operation == 'avg' or operation == 'mean':
            agg_value = sum(values) / len(values)
        elif operation == 'count':
            agg_value = len(values)
        elif operation == 'min':
            agg_value = min(values)
        elif operation == 'max':
            agg_value = max(values)
        else:
            agg_value = sum(values)

        result.append({
            group_by: key,
            value_field: agg_value,
            'count': len(values)
        })

    return sorted(result, key=lambda x: x[value_field], reverse=True)

def downsample_data(data: List[Dict], target_points: int) -> List[Dict]:
    """Downsample data to approximately target number of points"""
    if len(data) <= target_points:
        return data

    step = len(data) / target_points
    return [data[int(i * step)] for i in range(target_points)]

def calculate_percentages(data: List[Dict], value_field: str) -> List[Dict]:
    """Add percentage field based on value"""
    total = sum(float(row[value_field]) for row in data)

    result = []
    for row in data:
        new_row = row.copy()
        new_row['percentage'] = (float(row[value_field]) / total) * 100
        result.append(new_row)

    return result

def main():
    parser = argparse.ArgumentParser(description='Process data for visualization')
    parser.add_argument('input', type=str, help='Input CSV file')
    parser.add_argument('--to-json', type=str, help='Convert to JSON and save to file')
    parser.add_argument('--aggregate', type=str, help='Group by field')
    parser.add_argument('--value', type=str, help='Value field for aggregation')
    parser.add_argument('--operation', choices=['sum', 'avg', 'mean', 'count', 'min', 'max'],
                        default='sum', help='Aggregation operation')
    parser.add_argument('--downsample', type=int, help='Downsample to N points')
    parser.add_argument('--percentages', type=str, help='Calculate percentages for value field')
    parser.add_argument('--output', type=str, help='Output file')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        sys.exit(1)

    # Load data
    try:
        data = csv_to_json(input_path)
        print(f"✅ Loaded {len(data)} rows from {input_path}")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        sys.exit(1)

    # Process
    if args.aggregate:
        if not args.value:
            print("❌ Error: --value required for aggregation")
            sys.exit(1)
        data = aggregate_data(data, args.aggregate, args.value, args.operation)
        print(f"✅ Aggregated to {len(data)} groups")

    if args.downsample:
        data = downsample_data(data, args.downsample)
        print(f"✅ Downsampled to {len(data)} points")

    if args.percentages:
        data = calculate_percentages(data, args.percentages)
        print(f"✅ Added percentage calculations")

    # Output
    output_data = json.dumps(data, indent=2)

    if args.output or args.to_json:
        output_file = Path(args.output or args.to_json)
        output_file.write_text(output_data)
        print(f"✅ Saved to {output_file}")
    else:
        print("\nProcessed Data:")
        print(output_data)

if __name__ == "__main__":
    main()
```
