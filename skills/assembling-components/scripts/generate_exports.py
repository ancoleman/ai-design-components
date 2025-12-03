#!/usr/bin/env python3
"""
generate_exports.py - Barrel Export Generator

Generates index.ts barrel export files for React/TypeScript component directories.
Scans for .tsx files and creates proper exports.

ZERO CONTEXT TOKEN COST - Executed without loading into Claude's context.

Usage:
    python generate_exports.py <directory>

Examples:
    python generate_exports.py src/components
    python generate_exports.py src/components/ui
"""

import sys
import re
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class ExportInfo:
    """Information about an export."""
    name: str
    file_path: str
    is_default: bool


def find_exports(file_path: Path) -> List[ExportInfo]:
    """Find all exports in a TypeScript/TSX file."""
    exports = []
    content = file_path.read_text(encoding='utf-8')
    file_stem = file_path.stem

    # Check for default export
    # Patterns: export default function X, export default X, export default class X
    default_patterns = [
        r'export\s+default\s+function\s+(\w+)',
        r'export\s+default\s+class\s+(\w+)',
        r'export\s+default\s+(\w+)',
    ]

    for pattern in default_patterns:
        match = re.search(pattern, content)
        if match:
            name = match.group(1)
            # Use PascalCase version of filename if export name is generic
            if name in ('default', 'component', 'Component'):
                name = to_pascal_case(file_stem)
            exports.append(ExportInfo(
                name=name,
                file_path=f'./{file_stem}',
                is_default=True
            ))
            break

    # Check for named exports
    # Patterns: export function X, export const X, export class X, export type X, export interface X
    named_patterns = [
        r'export\s+(?:async\s+)?function\s+(\w+)',
        r'export\s+const\s+(\w+)',
        r'export\s+let\s+(\w+)',
        r'export\s+class\s+(\w+)',
        r'export\s+type\s+(\w+)',
        r'export\s+interface\s+(\w+)',
        r'export\s+enum\s+(\w+)',
    ]

    for pattern in named_patterns:
        for match in re.finditer(pattern, content):
            name = match.group(1)
            # Skip if it's a default export we already captured
            if any(e.name == name and e.is_default for e in exports):
                continue
            exports.append(ExportInfo(
                name=name,
                file_path=f'./{file_stem}',
                is_default=False
            ))

    return exports


def to_pascal_case(name: str) -> str:
    """Convert kebab-case or snake_case to PascalCase."""
    parts = re.split(r'[-_]', name)
    return ''.join(part.capitalize() for part in parts)


def generate_index_content(exports: List[ExportInfo]) -> str:
    """Generate the content for an index.ts barrel export file."""
    lines = []

    # Group exports by file
    files: dict[str, List[ExportInfo]] = {}
    for export in exports:
        if export.file_path not in files:
            files[export.file_path] = []
        files[export.file_path].append(export)

    # Generate export statements
    for file_path, file_exports in sorted(files.items()):
        default_exports = [e for e in file_exports if e.is_default]
        named_exports = [e for e in file_exports if not e.is_default]

        if default_exports and named_exports:
            # Both default and named exports
            names = ', '.join(e.name for e in named_exports)
            lines.append(f"export {{ default as {default_exports[0].name}, {names} }} from '{file_path}'")
        elif default_exports:
            # Only default export - re-export as named
            lines.append(f"export {{ {default_exports[0].name} }} from '{file_path}'")
        elif named_exports:
            # Only named exports
            names = ', '.join(e.name for e in named_exports)
            lines.append(f"export {{ {names} }} from '{file_path}'")

    return '\n'.join(sorted(lines)) + '\n'


def process_directory(directory: Path, recursive: bool = True) -> dict[Path, str]:
    """Process a directory and generate barrel exports."""
    results = {}

    # Find all directories with .tsx files
    if recursive:
        dirs_to_process = set()
        for tsx_file in directory.rglob('*.tsx'):
            if tsx_file.name != 'index.tsx':
                dirs_to_process.add(tsx_file.parent)
    else:
        dirs_to_process = {directory}

    for dir_path in dirs_to_process:
        exports = []

        # Find all .tsx files (excluding index.tsx)
        tsx_files = [f for f in dir_path.glob('*.tsx') if f.name != 'index.tsx']

        if not tsx_files:
            continue

        for tsx_file in tsx_files:
            file_exports = find_exports(tsx_file)
            if not file_exports:
                # If no exports found, assume default export with PascalCase name
                exports.append(ExportInfo(
                    name=to_pascal_case(tsx_file.stem),
                    file_path=f'./{tsx_file.stem}',
                    is_default=True
                ))
            else:
                exports.extend(file_exports)

        if exports:
            content = generate_index_content(exports)
            results[dir_path / 'index.ts'] = content

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Generate barrel export files for React/TypeScript components',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s src/components
  %(prog)s src/components/ui --no-recursive
  %(prog)s src/components --dry-run
        """
    )
    parser.add_argument('directory', type=Path, help='Directory to process')
    parser.add_argument('--no-recursive', action='store_true', help='Only process the specified directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated without writing')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing index.ts files')

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(1)

    results = process_directory(args.directory, recursive=not args.no_recursive)

    if not results:
        print("No components found to generate exports for.")
        sys.exit(0)

    print(f"\n{'=' * 60}")
    print(f"  BARREL EXPORT GENERATOR")
    print(f"{'=' * 60}\n")

    created = 0
    skipped = 0

    for index_path, content in sorted(results.items()):
        relative_path = index_path.relative_to(args.directory.parent) if args.directory.parent != index_path.parent else index_path.name

        if args.dry_run:
            print(f"  Would create: {relative_path}")
            print(f"  {'-' * 40}")
            for line in content.split('\n'):
                if line:
                    print(f"    {line}")
            print()
        else:
            if index_path.exists() and not args.overwrite:
                print(f"  Skipped (exists): {relative_path}")
                skipped += 1
            else:
                index_path.write_text(content, encoding='utf-8')
                print(f"  Created: {relative_path}")
                created += 1

    print(f"\n{'-' * 60}")
    if args.dry_run:
        print(f"  Dry run: {len(results)} files would be created")
    else:
        print(f"  Created: {created} files")
        if skipped:
            print(f"  Skipped: {skipped} files (use --overwrite to replace)")
    print()


if __name__ == "__main__":
    main()
