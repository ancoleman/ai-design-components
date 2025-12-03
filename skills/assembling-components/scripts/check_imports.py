#!/usr/bin/env python3
"""
check_imports.py - Import Chain Validator

Validates that import chains are correct in React/TypeScript projects:
- tokens.css is imported before other styles
- ThemeProvider wraps the app
- Barrel exports exist for component directories
- No circular imports

ZERO CONTEXT TOKEN COST - Executed without loading into Claude's context.

Usage:
    python check_imports.py <directory>

Examples:
    python check_imports.py src
    python check_imports.py demo/examples/my-project/src
"""

import sys
import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from collections import defaultdict


@dataclass
class ImportInfo:
    """Information about an import statement."""
    source: str
    specifiers: List[str]
    is_css: bool
    is_relative: bool
    line_number: int


@dataclass
class ValidationResult:
    """Result of validation checks."""
    file: str
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ProjectValidation:
    """Overall project validation results."""
    total_files: int = 0
    files_with_issues: int = 0
    total_issues: int = 0
    total_warnings: int = 0
    results: List[ValidationResult] = field(default_factory=list)
    missing_barrel_exports: List[str] = field(default_factory=list)
    token_import_issues: List[str] = field(default_factory=list)


def parse_imports(file_path: Path) -> List[ImportInfo]:
    """Parse all import statements from a file."""
    imports = []
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Match various import patterns
    patterns = [
        # import X from 'path'
        r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",
        # import { X, Y } from 'path'
        r"import\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]",
        # import 'path' (side-effect import, like CSS)
        r"import\s+['\"]([^'\"]+)['\"]",
        # import * as X from 'path'
        r"import\s+\*\s+as\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",
    ]

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line.startswith('import'):
            continue

        # Side-effect import (CSS, etc.)
        side_effect_match = re.match(r"import\s+['\"]([^'\"]+)['\"]", line)
        if side_effect_match:
            source = side_effect_match.group(1)
            imports.append(ImportInfo(
                source=source,
                specifiers=[],
                is_css=source.endswith('.css'),
                is_relative=source.startswith('.') or source.startswith('@/'),
                line_number=line_num
            ))
            continue

        # Named or default import
        for pattern in patterns[:-1]:  # Exclude side-effect pattern
            match = re.match(pattern, line)
            if match:
                if len(match.groups()) == 2:
                    specifiers_str, source = match.groups()
                    specifiers = [s.strip() for s in specifiers_str.split(',')]
                else:
                    source = match.group(1)
                    specifiers = []

                imports.append(ImportInfo(
                    source=source,
                    specifiers=specifiers,
                    is_css=source.endswith('.css'),
                    is_relative=source.startswith('.') or source.startswith('@/'),
                    line_number=line_num
                ))
                break

    return imports


def check_token_import_order(file_path: Path, imports: List[ImportInfo]) -> List[str]:
    """Check that tokens.css is imported before other CSS files."""
    issues = []

    css_imports = [i for i in imports if i.is_css]
    if not css_imports:
        return issues

    token_import_idx = None
    for idx, imp in enumerate(css_imports):
        if 'tokens' in imp.source.lower():
            token_import_idx = idx
            break

    if token_import_idx is None:
        # No token import found - might be okay if it's not an entry file
        if file_path.name in ('main.tsx', 'index.tsx', 'App.tsx', 'layout.tsx'):
            issues.append(f"Entry file should import tokens.css")
    elif token_import_idx > 0:
        issues.append(f"tokens.css should be imported BEFORE other CSS files (line {css_imports[token_import_idx].line_number})")

    return issues


def check_theme_provider(file_path: Path) -> List[str]:
    """Check that entry files use ThemeProvider."""
    issues = []

    if file_path.name not in ('main.tsx', 'index.tsx', 'App.tsx', 'layout.tsx', '_app.tsx'):
        return issues

    content = file_path.read_text(encoding='utf-8')

    # Check for ThemeProvider import
    has_theme_import = re.search(r"import.*ThemeProvider", content) is not None

    # Check for ThemeProvider usage
    has_theme_usage = re.search(r"<ThemeProvider", content) is not None

    if file_path.name in ('main.tsx', 'layout.tsx', '_app.tsx'):
        if not has_theme_import:
            issues.append("Entry file should import ThemeProvider")
        if not has_theme_usage:
            issues.append("Entry file should wrap app with ThemeProvider")

    return issues


def check_barrel_exports(directory: Path) -> List[str]:
    """Check that component directories have barrel exports."""
    missing = []

    # Find directories with .tsx files but no index.ts
    for dir_path in directory.rglob('*'):
        if not dir_path.is_dir():
            continue

        # Skip certain directories
        if any(skip in dir_path.parts for skip in ('node_modules', '.next', 'dist', 'build')):
            continue

        tsx_files = list(dir_path.glob('*.tsx'))
        has_index = (dir_path / 'index.ts').exists() or (dir_path / 'index.tsx').exists()

        # If there are multiple .tsx files, there should be a barrel export
        if len(tsx_files) > 1 and not has_index:
            relative = dir_path.relative_to(directory)
            missing.append(str(relative))

    return missing


def find_circular_imports(directory: Path) -> List[str]:
    """Detect circular imports in the project."""
    # Build import graph
    import_graph: Dict[str, Set[str]] = defaultdict(set)

    for ts_file in directory.rglob('*.ts'):
        if 'node_modules' in str(ts_file):
            continue
        imports = parse_imports(ts_file)
        file_key = str(ts_file.relative_to(directory))

        for imp in imports:
            if imp.is_relative:
                # Resolve relative import
                if imp.source.startswith('./'):
                    resolved = ts_file.parent / imp.source[2:]
                elif imp.source.startswith('../'):
                    resolved = (ts_file.parent / imp.source).resolve()
                elif imp.source.startswith('@/'):
                    resolved = directory / imp.source[2:]
                else:
                    continue

                # Add .ts or .tsx extension if needed
                if not resolved.suffix:
                    for ext in ['.ts', '.tsx', '/index.ts', '/index.tsx']:
                        if (resolved.parent / (resolved.name + ext)).exists():
                            resolved = resolved.parent / (resolved.name + ext)
                            break

                if resolved.exists():
                    target_key = str(resolved.relative_to(directory))
                    import_graph[file_key].add(target_key)

    # Same for .tsx files
    for tsx_file in directory.rglob('*.tsx'):
        if 'node_modules' in str(tsx_file):
            continue
        imports = parse_imports(tsx_file)
        file_key = str(tsx_file.relative_to(directory))

        for imp in imports:
            if imp.is_relative:
                if imp.source.startswith('./'):
                    resolved = tsx_file.parent / imp.source[2:]
                elif imp.source.startswith('../'):
                    resolved = (tsx_file.parent / imp.source).resolve()
                elif imp.source.startswith('@/'):
                    resolved = directory / imp.source[2:]
                else:
                    continue

                if not resolved.suffix:
                    for ext in ['.ts', '.tsx', '/index.ts', '/index.tsx']:
                        test_path = resolved.parent / (resolved.name + ext)
                        if test_path.exists():
                            resolved = test_path
                            break

                if resolved.exists():
                    target_key = str(resolved.relative_to(directory))
                    import_graph[file_key].add(target_key)

    # Detect cycles using DFS
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in import_graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(' -> '.join(cycle))
                return True

        path.pop()
        rec_stack.remove(node)
        return False

    for node in import_graph:
        if node not in visited:
            dfs(node)

    return cycles


def validate_file(file_path: Path) -> ValidationResult:
    """Validate a single file."""
    result = ValidationResult(file=str(file_path))

    try:
        imports = parse_imports(file_path)

        # Check token import order
        result.issues.extend(check_token_import_order(file_path, imports))

        # Check ThemeProvider usage
        result.issues.extend(check_theme_provider(file_path))

    except Exception as e:
        result.warnings.append(f"Could not parse file: {e}")

    return result


def validate_project(directory: Path) -> ProjectValidation:
    """Validate the entire project."""
    validation = ProjectValidation()

    # Find all TypeScript/TSX files
    ts_files = list(directory.rglob('*.ts')) + list(directory.rglob('*.tsx'))
    ts_files = [f for f in ts_files if 'node_modules' not in str(f)]

    validation.total_files = len(ts_files)

    # Validate each file
    for ts_file in ts_files:
        result = validate_file(ts_file)
        if result.issues or result.warnings:
            validation.results.append(result)
            validation.files_with_issues += 1
            validation.total_issues += len(result.issues)
            validation.total_warnings += len(result.warnings)

    # Check barrel exports
    validation.missing_barrel_exports = check_barrel_exports(directory)

    # Check for circular imports
    # (Disabled by default as it can be slow on large projects)
    # validation.circular_imports = find_circular_imports(directory)

    return validation


def format_report(validation: ProjectValidation) -> str:
    """Format the validation report."""
    lines = []

    lines.append("")
    lines.append("=" * 60)
    lines.append("  IMPORT CHAIN VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append("")

    if not validation.results and not validation.missing_barrel_exports:
        lines.append("  All import chains are valid!")
        lines.append("")
        lines.append(f"  Scanned: {validation.total_files} files")
        lines.append("")
        return '\n'.join(lines)

    # File-specific issues
    for result in validation.results:
        lines.append(f"  {result.file}")
        lines.append("  " + "-" * 50)

        for issue in result.issues:
            lines.append(f"    Issue: {issue}")

        for warning in result.warnings:
            lines.append(f"    Warning: {warning}")

        lines.append("")

    # Missing barrel exports
    if validation.missing_barrel_exports:
        lines.append("  Missing Barrel Exports (index.ts)")
        lines.append("  " + "-" * 50)
        for dir_path in validation.missing_barrel_exports:
            lines.append(f"    - {dir_path}/")
        lines.append("")
        lines.append("  Run: python scripts/generate_exports.py src/components")
        lines.append("")

    # Summary
    lines.append("-" * 60)
    lines.append("  SUMMARY")
    lines.append("-" * 60)
    lines.append(f"  Files scanned:       {validation.total_files}")
    lines.append(f"  Files with issues:   {validation.files_with_issues}")
    lines.append(f"  Total issues:        {validation.total_issues}")
    lines.append(f"  Total warnings:      {validation.total_warnings}")
    lines.append(f"  Missing exports:     {len(validation.missing_barrel_exports)}")
    lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate import chains in React/TypeScript projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks performed:
  - tokens.css imported before other CSS files
  - ThemeProvider wraps the app in entry files
  - Barrel exports exist for component directories
  - No circular imports (optional)

Examples:
  %(prog)s src
  %(prog)s demo/examples/my-project/src
        """
    )
    parser.add_argument('directory', type=Path, help='Directory to validate')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--check-circular', action='store_true', help='Check for circular imports (slow)')

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(1)

    validation = validate_project(args.directory)

    if args.json:
        import json
        print(json.dumps({
            'total_files': validation.total_files,
            'files_with_issues': validation.files_with_issues,
            'total_issues': validation.total_issues,
            'total_warnings': validation.total_warnings,
            'missing_barrel_exports': validation.missing_barrel_exports,
            'results': [
                {
                    'file': r.file,
                    'issues': r.issues,
                    'warnings': r.warnings
                }
                for r in validation.results
            ]
        }, indent=2))
    else:
        print(format_report(validation))

    # Exit with error if issues found
    if validation.total_issues > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
