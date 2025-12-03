#!/usr/bin/env python3
"""
validate_tokens.py - CSS Design Token Validator

Scans CSS files for hardcoded values that should use design tokens.
Returns actionable fix suggestions with specific token recommendations.

ZERO CONTEXT TOKEN COST - Executed without loading into Claude's context.

Usage:
    python validate_tokens.py <directory> [--strict] [--json] [--fix-suggestions]

Examples:
    python validate_tokens.py src/styles
    python validate_tokens.py src --strict --json
    python validate_tokens.py demo/examples/palo-alto-security-dashboard --fix-suggestions
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set
from collections import defaultdict


@dataclass
class Violation:
    """Represents a single token violation in a CSS file."""
    file: str
    line: int
    column: int
    property_name: str
    value: str
    category: str
    suggestion: str
    severity: str  # 'error' | 'warning' | 'info'
    fix: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report for a directory."""
    total_files: int
    files_with_violations: int
    total_violations: int
    errors: int
    warnings: int
    info: int
    violations: List[Violation]
    summary_by_category: Dict[str, int]


# ============================================================================
# TOKEN PATTERNS AND SUGGESTIONS
# ============================================================================

# Common token mappings for fix suggestions
TOKEN_MAPS = {
    'colors': {
        '#FA582D': '--color-cyber-orange',
        '#B23808': '--color-orange-dark',
        '#FF724D': '--color-orange-light',
        '#00C0E8': '--color-prisma-blue',
        '#00CC66': '--color-cortex-green',
        '#FFCB06': '--color-strata-yellow',
        '#C84727': '--color-unit42-red',
        '#FFFFFF': '--color-bg-primary',
        '#F8FAFC': '--color-bg-secondary',
        '#F1F5F9': '--color-bg-tertiary',
        '#1E293B': '--color-text-primary',
        '#64748B': '--color-text-secondary',
        '#94A3B8': '--color-text-tertiary',
        '#E2E8F0': '--color-border-primary',
        '#CBD5E1': '--color-border-secondary',
        '#0F172A': '--color-bg-primary (dark)',
        '#334155': '--color-bg-tertiary (dark)',
    },
    'spacing': {
        '4px': '--spacing-xs (--space-1)',
        '8px': '--spacing-sm (--space-2)',
        '12px': '--space-3',
        '16px': '--spacing-md (--space-4)',
        '20px': '--space-5',
        '24px': '--spacing-lg (--space-6)',
        '32px': '--spacing-xl (--space-8)',
        '40px': '--space-10',
        '48px': '--spacing-2xl (--space-12)',
        '64px': '--space-16',
    },
    'font-sizes': {
        '12px': '--font-size-xs',
        '14px': '--font-size-sm',
        '16px': '--font-size-base',
        '18px': '--font-size-lg',
        '20px': '--font-size-xl',
        '24px': '--font-size-2xl',
        '30px': '--font-size-3xl',
        '36px': '--font-size-4xl',
    },
    'radii': {
        '4px': '--radius-sm',
        '8px': '--radius-md',
        '12px': '--radius-lg',
        '16px': '--radius-xl',
        '9999px': '--radius-full',
    },
    'durations': {
        '150ms': '--duration-fast',
        '200ms': '--duration-normal',
        '300ms': '--duration-slow',
    },
}

# Validation rules with patterns
VALIDATION_RULES = {
    'hardcoded-colors': {
        'pattern': r'(?<!var\()(?<!-)#[0-9A-Fa-f]{3,8}\b',
        'property_pattern': r'(color|background|background-color|border|border-color|fill|stroke|box-shadow|text-shadow|outline)',
        'suggestion': 'Use semantic color token (e.g., --color-primary, --color-text-primary)',
        'severity': 'error',
        'category': 'colors',
    },
    'rgb-colors': {
        'pattern': r'(?<!var\()rgba?\([^)]+\)',
        'suggestion': 'Use semantic color token instead of rgb/rgba',
        'severity': 'error',
        'category': 'colors',
    },
    'hardcoded-spacing': {
        'pattern': r'(?<!var\()(?<!:)\b(\d{2,})(px)\b',
        'property_pattern': r'(padding|margin|gap|top|right|bottom|left|width|height|min-width|max-width|min-height|max-height)',
        'suggestion': 'Use spacing token (e.g., --spacing-md, --spacing-lg)',
        'severity': 'error',
        'category': 'spacing',
        'min_value': 4,  # Only flag values >= 4px
    },
    'hardcoded-font-sizes': {
        'pattern': r'font-size:\s*(\d+)(px|rem)',
        'suggestion': 'Use font-size token (e.g., --font-size-sm, --font-size-base)',
        'severity': 'error',
        'category': 'font-sizes',
    },
    'hardcoded-border-radius': {
        'pattern': r'border-radius:\s*(\d+)(px)',
        'suggestion': 'Use radius token (e.g., --radius-md, --radius-lg)',
        'severity': 'warning',
        'category': 'radii',
    },
    'hardcoded-box-shadow': {
        'pattern': r'box-shadow:\s*\d+px\s+\d+px[^;]*(?!var\()',
        'suggestion': 'Use shadow token (e.g., --shadow-sm, --shadow-md)',
        'severity': 'warning',
        'category': 'shadows',
    },
    'hardcoded-transitions': {
        'pattern': r'transition[^:]*:\s*(?!var\()(?!none)(?!inherit)[^;]*\d+(ms|s)',
        'suggestion': 'Use transition token (e.g., --transition-fast, --transition-normal)',
        'severity': 'info',
        'category': 'transitions',
    },
    'hardcoded-z-index': {
        'pattern': r'z-index:\s*(\d{3,})',
        'suggestion': 'Use z-index token (e.g., --z-dropdown, --z-modal)',
        'severity': 'warning',
        'category': 'z-index',
    },
}

# Patterns to skip (not violations)
SKIP_PATTERNS = [
    r'^\s*--',           # CSS custom property definitions
    r'^\s*/\*',          # Comment start
    r'^\s*\*',           # Comment continuation
    r'currentColor',     # CSS keyword
    r'transparent',      # CSS keyword
    r'inherit',          # CSS keyword
    r'initial',          # CSS keyword
    r'unset',            # CSS keyword
    r'@media',           # Media query line (breakpoints allowed)
    r'@keyframes',       # Keyframe definitions
    r'from\s*{',         # Keyframe from
    r'to\s*{',           # Keyframe to
    r'\d+%\s*{',         # Keyframe percentage
]

# Properties where hardcoded values are acceptable
EXCEPTION_PROPERTIES = [
    'outline',           # Accessibility focus indicators
    'outline-offset',    # Accessibility
    'transform',         # Animation transforms
    'animation',         # Animation definitions
    'content',           # Pseudo-element content
    'clip-path',         # Complex clipping
    'mask',              # Complex masking
]

# Values that are always acceptable
EXCEPTION_VALUES = [
    '0',
    '0px',
    '1px',              # Hairline borders
    '2px',              # Focus outlines
    '100%',
    '50%',
    'auto',
    'none',
    'inherit',
    'initial',
    'unset',
    'currentColor',
    'transparent',
]

# Layout values that are acceptable (container widths, breakpoints)
LAYOUT_EXCEPTION_VALUES = [
    '1400px',           # Common max-width container
    '1200px',           # Common max-width container
    '1024px',           # Common max-width container
    '768px',            # Tablet breakpoint
    '640px',            # Mobile breakpoint
    '480px',            # Small mobile breakpoint
]

# Patterns in lines to skip entirely
LINE_SKIP_PATTERNS = [
    r'max-width:\s*\d+px',     # Container max-widths
    r'min-width:\s*\d+px',     # Container min-widths
    r'minmax\(',               # Grid minmax functions
    r'grid-template',          # Grid templates
    r'repeat\(',               # Grid repeat
]


# ============================================================================
# VALIDATION LOGIC
# ============================================================================

def should_skip_line(line: str) -> bool:
    """Check if a line should be skipped from validation."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    # Also skip layout-specific patterns
    for pattern in LINE_SKIP_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def is_exception_property(line: str) -> bool:
    """Check if the line contains an exception property."""
    for prop in EXCEPTION_PROPERTIES:
        if f'{prop}:' in line or f'{prop} :' in line:
            return True
    return False


def is_exception_value(value: str) -> bool:
    """Check if a value is in the exception list."""
    return value.strip() in EXCEPTION_VALUES


def get_token_suggestion(value: str, category: str) -> Optional[str]:
    """Get specific token suggestion for a hardcoded value."""
    if category in TOKEN_MAPS:
        # Normalize the value for lookup
        normalized = value.upper().strip()
        for hardcoded, token in TOKEN_MAPS[category].items():
            if hardcoded.upper() == normalized or hardcoded == value:
                return f'var({token})'
    return None


def validate_file(filepath: Path, strict: bool = False) -> List[Violation]:
    """Validate a single CSS file for token violations."""
    violations = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return violations

    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Skip lines that shouldn't be validated
        if should_skip_line(line):
            continue

        # Skip exception properties
        if is_exception_property(line):
            continue

        # Check each validation rule
        for rule_name, rule in VALIDATION_RULES.items():
            pattern = rule['pattern']
            matches = list(re.finditer(pattern, line, re.IGNORECASE))

            for match in matches:
                value = match.group(0)
                column = match.start() + 1

                # Skip exception values
                if is_exception_value(value):
                    continue

                # For spacing, check minimum value
                if 'min_value' in rule:
                    num_match = re.search(r'(\d+)', value)
                    if num_match and int(num_match.group(1)) < rule['min_value']:
                        continue

                # Skip if already using var()
                if 'var(' in line[max(0, match.start()-4):match.start()]:
                    continue

                # Get specific token suggestion if available
                specific_fix = get_token_suggestion(value, rule['category'])

                # Skip non-strict warnings in non-strict mode
                if not strict and rule['severity'] in ['info']:
                    continue

                violations.append(Violation(
                    file=str(filepath),
                    line=line_num,
                    column=column,
                    property_name=rule_name,
                    value=value,
                    category=rule['category'],
                    suggestion=rule['suggestion'],
                    severity=rule['severity'],
                    fix=specific_fix
                ))

    return violations


def validate_directory(directory: Path, strict: bool = False) -> ValidationReport:
    """Validate all CSS files in a directory."""
    css_files = list(directory.rglob('*.css'))

    all_violations: List[Violation] = []
    files_with_violations: Set[str] = set()
    summary_by_category: Dict[str, int] = defaultdict(int)

    for css_file in css_files:
        # Skip token definition files
        if 'tokens' in css_file.name.lower():
            continue

        violations = validate_file(css_file, strict)

        if violations:
            files_with_violations.add(str(css_file))
            all_violations.extend(violations)

            for v in violations:
                summary_by_category[v.category] += 1

    errors = sum(1 for v in all_violations if v.severity == 'error')
    warnings = sum(1 for v in all_violations if v.severity == 'warning')
    info = sum(1 for v in all_violations if v.severity == 'info')

    return ValidationReport(
        total_files=len(css_files),
        files_with_violations=len(files_with_violations),
        total_violations=len(all_violations),
        errors=errors,
        warnings=warnings,
        info=info,
        violations=all_violations,
        summary_by_category=dict(summary_by_category)
    )


# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def format_console_report(report: ValidationReport, show_fixes: bool = False) -> str:
    """Format the validation report for console output."""
    lines = []

    lines.append("")
    lines.append("=" * 70)
    lines.append("  CSS DESIGN TOKEN VALIDATION REPORT")
    lines.append("=" * 70)
    lines.append("")

    if not report.violations:
        lines.append("  All CSS files use design tokens correctly!")
        lines.append("")
        lines.append(f"  Scanned: {report.total_files} files")
        lines.append("")
        return '\n'.join(lines)

    # Group violations by file
    by_file: Dict[str, List[Violation]] = defaultdict(list)
    for v in report.violations:
        by_file[v.file].append(v)

    for filepath, violations in by_file.items():
        lines.append(f"  {filepath}")
        lines.append("  " + "-" * 60)

        for v in violations:
            icon = {"error": "", "warning": "", "info": ""}.get(v.severity, "")
            lines.append(f"    {icon} Line {v.line}:{v.column} [{v.severity.upper()}]")
            lines.append(f"       Found: {v.value}")
            lines.append(f"       Rule: {v.category}")
            lines.append(f"       Fix: {v.suggestion}")
            if show_fixes and v.fix:
                lines.append(f"       Suggested: {v.fix}")
            lines.append("")

        lines.append("")

    # Summary
    lines.append("-" * 70)
    lines.append("  SUMMARY")
    lines.append("-" * 70)
    lines.append(f"  Files scanned:     {report.total_files}")
    lines.append(f"  Files with issues: {report.files_with_violations}")
    lines.append(f"  Total violations:  {report.total_violations}")
    lines.append(f"    - Errors:   {report.errors}")
    lines.append(f"    - Warnings: {report.warnings}")
    lines.append(f"    - Info:     {report.info}")
    lines.append("")

    if report.summary_by_category:
        lines.append("  By Category:")
        for category, count in sorted(report.summary_by_category.items()):
            lines.append(f"    - {category}: {count}")
        lines.append("")

    return '\n'.join(lines)


def format_json_report(report: ValidationReport) -> str:
    """Format the validation report as JSON."""
    return json.dumps({
        'total_files': report.total_files,
        'files_with_violations': report.files_with_violations,
        'total_violations': report.total_violations,
        'errors': report.errors,
        'warnings': report.warnings,
        'info': report.info,
        'summary_by_category': report.summary_by_category,
        'violations': [asdict(v) for v in report.violations]
    }, indent=2)


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Validate CSS files for design token usage',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s src/styles
  %(prog)s src --strict --json
  %(prog)s demo/examples --fix-suggestions
        """
    )
    parser.add_argument('directory', type=Path, help='Directory to scan')
    parser.add_argument('--strict', action='store_true',
                        help='Include info-level violations')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--fix-suggestions', action='store_true',
                        help='Show specific token suggestions where available')

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(2)

    report = validate_directory(args.directory, strict=args.strict)

    if args.json:
        print(format_json_report(report))
    else:
        print(format_console_report(report, show_fixes=args.fix_suggestions))

    # Exit with appropriate code
    if report.errors > 0:
        sys.exit(1)
    elif report.warnings > 0:
        sys.exit(0)  # Warnings don't fail the build
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
