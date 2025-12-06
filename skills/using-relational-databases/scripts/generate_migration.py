#!/usr/bin/env python3
"""
Migration Template Generator

Generates migration templates for common database operations.
Provides safe patterns for adding/dropping columns, creating indexes, etc.

Usage:
    python generate_migration.py add-column users email varchar
    python generate_migration.py add-index users email
    python generate_migration.py create-table posts
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


TEMPLATES = {
    "add-column": """-- Migration: {name}
-- Created: {timestamp}

-- Phase 1: Add column (safe, allows NULL)
ALTER TABLE {table} ADD COLUMN {column} {type};

-- Phase 2: Backfill data (if needed)
-- UPDATE {table} SET {column} = ... WHERE {column} IS NULL;

-- Phase 3: Add constraints (after backfill complete)
-- ALTER TABLE {table} ALTER COLUMN {column} SET NOT NULL;
-- ALTER TABLE {table} ADD CONSTRAINT check_{column} CHECK (...);

-- Rollback
-- ALTER TABLE {table} DROP COLUMN {column};
""",

    "drop-column": """-- Migration: {name}
-- Created: {timestamp}
-- WARNING: This is a multi-phase migration for zero-downtime deployment

-- Phase 1: Make column nullable (deploy code that doesn't use this column)
ALTER TABLE {table} ALTER COLUMN {column} DROP NOT NULL;

-- Phase 2: Remove constraints (deploy)
-- ALTER TABLE {table} DROP CONSTRAINT constraint_name;

-- Phase 3: Drop column (after confirming code doesn't use it)
-- ALTER TABLE {table} DROP COLUMN {column};

-- Rollback (Phase 1 only)
-- ALTER TABLE {table} ALTER COLUMN {column} SET NOT NULL;
""",

    "add-index": """-- Migration: {name}
-- Created: {timestamp}

-- Create index concurrently (does not block writes)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_{table}_{column}
ON {table}({column});

-- For composite index:
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_{table}_{column}_other
-- ON {table}({column}, other_column);

-- Rollback
-- DROP INDEX CONCURRENTLY IF EXISTS idx_{table}_{column};
""",

    "create-table": """-- Migration: {name}
-- Created: {timestamp}

CREATE TABLE {table} (
    id SERIAL PRIMARY KEY,
    -- Add your columns here
    -- email VARCHAR(255) UNIQUE NOT NULL,
    -- name VARCHAR(255) NOT NULL,

    -- Timestamps (recommended)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
-- CREATE INDEX idx_{table}_column ON {table}(column);

-- Create trigger for updated_at (optional)
CREATE TRIGGER update_{table}_updated_at
    BEFORE UPDATE ON {table}
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Rollback
-- DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};
-- DROP TABLE {table};
""",

    "add-foreign-key": """-- Migration: {name}
-- Created: {timestamp}

-- Add foreign key column
ALTER TABLE {table} ADD COLUMN {column} INTEGER;

-- Create index on foreign key (important for performance)
CREATE INDEX CONCURRENTLY idx_{table}_{column} ON {table}({column});

-- Add foreign key constraint
ALTER TABLE {table}
ADD CONSTRAINT fk_{table}_{column}
FOREIGN KEY ({column})
REFERENCES {ref_table}(id)
ON DELETE CASCADE;  -- Or: RESTRICT, SET NULL, SET DEFAULT

-- Rollback
-- ALTER TABLE {table} DROP CONSTRAINT fk_{table}_{column};
-- DROP INDEX CONCURRENTLY idx_{table}_{column};
-- ALTER TABLE {table} DROP COLUMN {column};
""",

    "rename-column": """-- Migration: {name}
-- Created: {timestamp}
-- WARNING: Multi-phase migration for zero-downtime

-- Phase 1: Add new column
ALTER TABLE {table} ADD COLUMN {new_column} {type};

-- Phase 2: Backfill data (deploy code writing to both columns)
UPDATE {table} SET {new_column} = {column} WHERE {new_column} IS NULL;

-- Phase 3: Make new column NOT NULL (after backfill)
-- ALTER TABLE {table} ALTER COLUMN {new_column} SET NOT NULL;

-- Phase 4: Drop old column (deploy code using only new column)
-- ALTER TABLE {table} DROP COLUMN {column};

-- Rollback (Phase 1-2)
-- ALTER TABLE {table} DROP COLUMN {new_column};
""",
}


def generate_migration(operation: str, args: argparse.Namespace):
    """Generate migration file for the specified operation."""
    if operation not in TEMPLATES:
        print(f"Error: Unknown operation '{operation}'")
        print(f"Available operations: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)

    template = TEMPLATES[operation]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Build context for template
    context = {
        "name": f"{operation}_{args.table}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "table": args.table,
    }

    if args.column:
        context["column"] = args.column
    if args.type:
        context["type"] = args.type
    if args.new_column:
        context["new_column"] = args.new_column
    if args.ref_table:
        context["ref_table"] = args.ref_table

    # Fill template
    try:
        migration = template.format(**context)
    except KeyError as e:
        print(f"Error: Missing required argument: {e}")
        sys.exit(1)

    # Output
    if args.output:
        filename = f"{timestamp}_{operation}_{args.table}.sql"
        filepath = Path(args.output) / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(migration)
        print(f"✅ Generated migration: {filepath}")
    else:
        print(migration)


def main():
    parser = argparse.ArgumentParser(
        description="Generate database migration templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add column
  python generate_migration.py add-column users email --type "VARCHAR(255)"

  # Add index
  python generate_migration.py add-index users email

  # Create table
  python generate_migration.py create-table posts

  # Add foreign key
  python generate_migration.py add-foreign-key posts author_id --ref-table users

  # Rename column (multi-phase)
  python generate_migration.py rename-column users email --new-column user_email --type "VARCHAR(255)"

  # Save to file
  python generate_migration.py add-column users email --type "VARCHAR(255)" -o migrations/
        """
    )

    parser.add_argument(
        "operation",
        choices=list(TEMPLATES.keys()),
        help="Migration operation type"
    )
    parser.add_argument(
        "table",
        help="Table name"
    )
    parser.add_argument(
        "column",
        nargs="?",
        help="Column name (if applicable)"
    )
    parser.add_argument(
        "--type",
        help="Column type (e.g., VARCHAR(255), INTEGER)"
    )
    parser.add_argument(
        "--new-column",
        help="New column name (for rename-column)"
    )
    parser.add_argument(
        "--ref-table",
        help="Referenced table (for add-foreign-key)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for migration file"
    )

    args = parser.parse_args()
    generate_migration(args.operation, args)


if __name__ == "__main__":
    main()
