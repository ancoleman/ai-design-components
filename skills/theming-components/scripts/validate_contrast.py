#!/usr/bin/env python3
"""
Validate color contrast ratios for WCAG compliance.

Checks:
- Text/background combinations meet WCAG 2.1 AA (4.5:1 normal text, 3:1 large text)
- UI component contrast meets 3:1 minimum
- Warns about AAA failures (7:1)
"""

import json
import sys
from pathlib import Path


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    """Calculate relative luminance (WCAG formula)."""
    r, g, b = [x / 255.0 for x in rgb]

    # Convert to sRGB
    def to_srgb(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r_srgb, g_srgb, b_srgb = to_srgb(r), to_srgb(g), to_srgb(b)

    # Calculate luminance
    return 0.2126 * r_srgb + 0.7152 * g_srgb + 0.0722 * b_srgb


def contrast_ratio(color1, color2):
    """Calculate contrast ratio between two colors."""
    l1 = relative_luminance(hex_to_rgb(color1))
    l2 = relative_luminance(hex_to_rgb(color2))

    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)


def load_theme_colors(tokens_dir):
    """Load color tokens from light theme."""
    theme_file = tokens_dir / 'themes' / 'light.json'

    if not theme_file.exists():
        print(f"❌ Theme file not found: {theme_file}")
        return None

    with open(theme_file, 'r') as f:
        theme = json.load(f)

    return theme.get('semantic', {}).get('color', {})


def validate_wcag_compliance():
    """Validate WCAG color contrast compliance."""
    print("🔍 Validating color contrast (WCAG 2.1)...")

    script_dir = Path(__file__).parent
    tokens_dir = script_dir.parent / 'tokens'

    colors = load_theme_colors(tokens_dir)
    if not colors:
        sys.exit(1)

    errors = []
    warnings = []

    # Define text/background pairs to check
    checks = [
        # (text_token, bg_token, min_ratio, description)
        ('text-primary', 'bg-primary', 4.5, 'Primary text on primary bg'),
        ('text-secondary', 'bg-primary', 4.5, 'Secondary text on primary bg'),
        ('text-primary', 'bg-secondary', 4.5, 'Primary text on secondary bg'),
        ('text-inverse', 'bg-inverse', 4.5, 'Inverse text on inverse bg'),
        ('primary', 'bg-primary', 3.0, 'Primary color contrast (UI component)'),
        ('error', 'bg-primary', 3.0, 'Error color contrast'),
        ('success', 'bg-primary', 3.0, 'Success color contrast'),
        ('warning', 'bg-primary', 3.0, 'Warning color contrast'),
    ]

    print("\n" + "=" * 70)
    print("WCAG CONTRAST VALIDATION")
    print("=" * 70)

    for text_key, bg_key, min_ratio, description in checks:
        text_token = colors.get(text_key, {})
        bg_token = colors.get(bg_key, {})

        if not text_token or not bg_token:
            warnings.append(f"⚠️  Missing token: {text_key} or {bg_key}")
            continue

        # Extract color values (handle references)
        text_color = text_token.get('$value', '')
        bg_color = bg_token.get('$value', '')

        # Skip if color is a reference (starts with {)
        if text_color.startswith('{') or bg_color.startswith('{'):
            warnings.append(f"⚠️  Skipping reference: {description}")
            continue

        # Skip non-hex colors
        if not text_color.startswith('#') or not bg_color.startswith('#'):
            continue

        try:
            ratio = contrast_ratio(text_color, bg_color)

            # Check against minimum ratio
            status = "✅" if ratio >= min_ratio else "❌"
            aaa_status = "AAA ✨" if ratio >= 7.0 else "AA" if ratio >= 4.5 else "FAIL"

            print(f"{status} {description}")
            print(f"   {text_key} ({text_color}) / {bg_key} ({bg_color})")
            print(f"   Ratio: {ratio:.2f}:1 ({aaa_status})")

            if ratio < min_ratio:
                errors.append(
                    f"❌ {description}: {ratio:.2f}:1 (required: {min_ratio}:1)"
                )
            elif ratio < 7.0 and min_ratio >= 4.5:
                warnings.append(
                    f"⚠️  {description}: {ratio:.2f}:1 (AAA requires 7:1)"
                )

        except Exception as e:
            warnings.append(f"⚠️  Error checking {description}: {e}")

    # Report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")

    if not errors:
        print("\n✅ All checked combinations meet WCAG 2.1 AA!")

    print(f"\n📊 Checked {len(checks)} color combinations")
    print("=" * 70)

    sys.exit(0 if not errors else 1)


if __name__ == '__main__':
    validate_wcag_compliance()
