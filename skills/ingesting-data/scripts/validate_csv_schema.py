#!/usr/bin/env python3
"""
CSV Schema Validation Tool

Validates CSV files against expected schema before ingestion.
Checks column names, data types, and value constraints.

Usage:
    python validate_csv_schema.py --file data.csv --schema schema.json
    python validate_csv_schema.py --file data.csv --columns id:int,name:str,amount:float
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

try:
    import polars as pl
except ImportError:
    print("Error: polars library not installed")
    print("Install with: pip install polars")
    sys.exit(1)


def parse_column_spec(spec: str) -> Dict[str, str]:
    """Parse column:type specification."""
    columns = {}
    for item in spec.split(","):
        name, dtype = item.split(":")
        columns[name.strip()] = dtype.strip()
    return columns


def validate_columns(df: pl.DataFrame, expected: Dict[str, str]) -> List[str]:
    """Validate column names and types."""
    errors = []

    # Check for missing columns
    for col in expected:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    # Check for extra columns
    for col in df.columns:
        if col not in expected:
            errors.append(f"Unexpected column: {col}")

    # Check types
    type_map = {
        "int": [pl.Int8, pl.Int16, pl.Int32, pl.Int64],
        "float": [pl.Float32, pl.Float64],
        "str": [pl.Utf8, pl.String],
        "bool": [pl.Boolean],
        "date": [pl.Date],
        "datetime": [pl.Datetime],
    }

    for col, expected_type in expected.items():
        if col in df.columns:
            actual_type = df[col].dtype
            valid_types = type_map.get(expected_type, [])

            if valid_types and actual_type not in valid_types:
                errors.append(
                    f"Column '{col}': expected {expected_type}, got {actual_type}"
                )

    return errors


def validate_nulls(df: pl.DataFrame, required: List[str]) -> List[str]:
    """Check for null values in required columns."""
    errors = []

    for col in required:
        if col in df.columns:
            null_count = df[col].null_count()
            if null_count > 0:
                errors.append(f"Column '{col}' has {null_count} null values")

    return errors


def validate_unique(df: pl.DataFrame, unique: List[str]) -> List[str]:
    """Check for unique constraints."""
    errors = []

    for col in unique:
        if col in df.columns:
            total = len(df)
            unique_count = df[col].n_unique()
            if unique_count < total:
                errors.append(
                    f"Column '{col}' has {total - unique_count} duplicate values"
                )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate CSV file against schema"
    )
    parser.add_argument(
        "--file",
        type=Path,
        required=True,
        help="CSV file to validate"
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="JSON schema file"
    )
    parser.add_argument(
        "--columns",
        help="Column spec (e.g., id:int,name:str,amount:float)"
    )
    parser.add_argument(
        "--required",
        help="Comma-separated list of required (non-null) columns"
    )
    parser.add_argument(
        "--unique",
        help="Comma-separated list of unique columns"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=1000,
        help="Number of rows to sample for validation (default: 1000)"
    )

    args = parser.parse_args()

    # Load CSV
    try:
        df = pl.read_csv(args.file, n_rows=args.sample)
        print(f"Loaded {len(df)} rows from {args.file}")
        print(f"Columns: {df.columns}")
        print("")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    all_errors = []

    # Load schema
    if args.schema:
        with open(args.schema) as f:
            schema = json.load(f)
        expected_columns = schema.get("columns", {})
        required = schema.get("required", [])
        unique = schema.get("unique", [])
    elif args.columns:
        expected_columns = parse_column_spec(args.columns)
        required = args.required.split(",") if args.required else []
        unique = args.unique.split(",") if args.unique else []
    else:
        print("Error: Either --schema or --columns must be provided")
        sys.exit(1)

    # Validate columns
    print("Validating columns...")
    all_errors.extend(validate_columns(df, expected_columns))

    # Validate nulls
    if required:
        print("Checking required columns...")
        all_errors.extend(validate_nulls(df, required))

    # Validate unique
    if unique:
        print("Checking unique constraints...")
        all_errors.extend(validate_unique(df, unique))

    # Print results
    print("")
    if all_errors:
        print("Validation FAILED:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Validation PASSED")
        print("")
        print("Schema summary:")
        for col in df.columns:
            print(f"  {col}: {df[col].dtype}")
        sys.exit(0)


if __name__ == "__main__":
    main()
