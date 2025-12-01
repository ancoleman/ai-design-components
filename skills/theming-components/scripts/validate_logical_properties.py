#!/usr/bin/env python3
"""
Validate that tokens use CSS logical properties for RTL support.

Checks:
- Token names use 'inline' instead of 'left/right'
- Token names use 'block' instead of 'top/bottom'
- No physical directional properties in token names
"""

import json
import sys
from pathlib import Path


def validate_logical_properties():
    """Validate CSS logical property usage in token names."""
    print("🔍 Validating CSS logical properties (RTL support)...")

    script_dir = Path(__file__).parent
    tokens_dir = script_dir.parent / 'tokens'

    errors = []
    warnings = []

    # Physical properties to avoid
    physical_terms = {
        'left', 'right', 'top', 'bottom',
        'horizontal', 'vertical'
    }

    # Logical properties (acceptable)
    logical_terms = {
        'inline', 'block', 'inline-start', 'inline-end',
        'block-start', 'block-end', 'inset'
    }

    def check_token_names(node, path=[]):
        """Recursively check token names."""
        if not isinstance(node, dict):
            return

        for key, value in node.items():
            if key.startswith('$'):  # Skip metadata
                continue

            current_path = path + [key]
            key_lower = key.lower()

            # Check for physical properties
            for physical in physical_terms:
                if physical in key_lower:
                    # Exception: Allow 'inset-inline-start' even though it contains 'start'
                    if any(logical in key_lower for logical in logical_terms):
                        continue

                    errors.append(
                        f"❌ Token uses physical property '{physical}': {'.'.join(current_path)}"
                    )
                    break

            # Recurse
            check_token_names(value, current_path)

    # Check all token files
    token_files_checked = 0
    for json_file in tokens_dir.rglob('*.json'):
        try:
            with open(json_file, 'r') as f:
                tokens = json.load(f)
                check_token_names(tokens)
                token_files_checked += 1
        except json.JSONDecodeError as e:
            warnings.append(f"⚠️  Invalid JSON in {json_file}: {e}")

    # Report
    print("\n" + "=" * 70)
    print("RTL VALIDATION REPORT")
    print("=" * 70)

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  {error}")
        print("\n💡 Tip: Use logical properties for RTL support:")
        print("  ✅ Use: inline, block, inline-start, inline-end")
        print("  ❌ Avoid: left, right, top, bottom")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")

    if not errors and not warnings:
        print("\n✅ All tokens use CSS logical properties! RTL-ready.")

    print(f"\n📊 Checked {token_files_checked} token files")
    print("=" * 70)

    sys.exit(0 if not errors else 1)


if __name__ == '__main__':
    validate_logical_properties()
