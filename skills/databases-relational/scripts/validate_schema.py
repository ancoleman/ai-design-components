#!/usr/bin/env python3
"""
Database Schema Validator

Validates database schema structure, constraints, and indexes.
Checks for common issues like missing indexes, lack of constraints, and naming conventions.

Usage:
    python validate_schema.py postgresql://user:pass@localhost/db
    python validate_schema.py postgresql://user:pass@localhost/db --table users
"""

import argparse
import sys
from typing import List, Dict, Any
from urllib.parse import urlparse

try:
    import sqlalchemy
    from sqlalchemy import create_engine, inspect, MetaData
except ImportError:
    print("Error: SQLAlchemy not installed. Run: pip install sqlalchemy")
    sys.exit(1)


class SchemaValidator:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.inspector = inspect(self.engine)
        self.issues = []
        self.warnings = []

    def validate_all(self, table_name: str = None) -> bool:
        """Run all validation checks."""
        print(f"Validating database schema: {self._get_db_name()}\n")

        tables = [table_name] if table_name else self.inspector.get_table_names()

        if not tables:
            print("Error: No tables found in database")
            return False

        for table in tables:
            print(f"Checking table: {table}")
            self._validate_table(table)

        self._print_results()
        return len(self.issues) == 0

    def _validate_table(self, table_name: str):
        """Validate a single table."""
        # Check primary key
        pk = self.inspector.get_pk_constraint(table_name)
        if not pk or not pk.get('constrained_columns'):
            self.issues.append(f"  ❌ {table_name}: No primary key defined")
        else:
            print(f"  ✓ Primary key: {pk['constrained_columns']}")

        # Check for timestamps
        columns = {col['name']: col for col in self.inspector.get_columns(table_name)}
        has_created_at = any('created' in name.lower() for name in columns.keys())
        has_updated_at = any('updated' in name.lower() for name in columns.keys())

        if not has_created_at:
            self.warnings.append(f"  ⚠️  {table_name}: No created_at timestamp column")
        if not has_updated_at:
            self.warnings.append(f"  ⚠️  {table_name}: No updated_at timestamp column")

        # Check foreign keys
        fks = self.inspector.get_foreign_keys(table_name)
        for fk in fks:
            fk_cols = fk['constrained_columns']
            ref_table = fk['referred_table']
            ref_cols = fk['referred_columns']
            print(f"  ✓ Foreign key: {fk_cols} → {ref_table}({ref_cols})")

            # Check if foreign key has index
            indexes = self.inspector.get_indexes(table_name)
            fk_indexed = any(
                set(fk_cols).issubset(set(idx['column_names']))
                for idx in indexes
            )
            if not fk_indexed:
                self.warnings.append(
                    f"  ⚠️  {table_name}: Foreign key {fk_cols} not indexed (slow joins)"
                )

        # Check unique constraints
        unique_constraints = self.inspector.get_unique_constraints(table_name)
        for uc in unique_constraints:
            print(f"  ✓ Unique constraint: {uc['column_names']}")

        # Check indexes
        indexes = self.inspector.get_indexes(table_name)
        if not indexes:
            self.warnings.append(f"  ⚠️  {table_name}: No indexes defined")
        else:
            for idx in indexes:
                print(f"  ✓ Index: {idx['name']} on {idx['column_names']}")

        # Check nullable constraints
        for col_name, col_info in columns.items():
            if col_name.endswith('_id') and col_info.get('nullable', True):
                self.warnings.append(
                    f"  ⚠️  {table_name}.{col_name}: Foreign key should be NOT NULL"
                )

        # Check naming conventions
        self._check_naming_conventions(table_name, columns)

    def _check_naming_conventions(self, table_name: str, columns: Dict):
        """Check if table and column names follow conventions."""
        # Table name should be plural lowercase
        if table_name != table_name.lower():
            self.warnings.append(
                f"  ⚠️  {table_name}: Table name should be lowercase"
            )

        # Column names should be snake_case
        for col_name in columns.keys():
            if col_name != col_name.lower():
                self.warnings.append(
                    f"  ⚠️  {table_name}.{col_name}: Column name should be lowercase"
                )
            if ' ' in col_name or '-' in col_name:
                self.issues.append(
                    f"  ❌ {table_name}.{col_name}: Column name contains invalid characters"
                )

    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)

        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(issue)

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(warning)

        if not self.issues and not self.warnings:
            print("\n✅ All checks passed! Schema looks good.")
        elif not self.issues:
            print(f"\n✅ No critical issues found (but {len(self.warnings)} warnings)")
        else:
            print(f"\n❌ Found {len(self.issues)} critical issues")

    def _get_db_name(self) -> str:
        """Extract database name from URL."""
        parsed = urlparse(self.database_url)
        return parsed.path.lstrip('/')


def main():
    parser = argparse.ArgumentParser(
        description="Validate database schema structure and constraints"
    )
    parser.add_argument(
        "database_url",
        help="Database connection URL (e.g., postgresql://user:pass@localhost/db)"
    )
    parser.add_argument(
        "--table",
        help="Validate specific table only",
        default=None
    )

    args = parser.parse_args()

    try:
        validator = SchemaValidator(args.database_url)
        success = validator.validate_all(args.table)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
