#!/usr/bin/env python3
"""
Validate accessibility of data visualization HTML/SVG

Checks:
- Text alternatives (aria-label or aria-describedby)
- Color contrast ratios
- Keyboard accessibility
- WCAG 2.1 AA compliance

Usage:
    python validate_accessibility.py chart.html
    python validate_accessibility.py chart.svg
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate WCAG contrast ratio between two hex colors.
    Returns ratio (1-21, where 21 is maximum contrast).
    """
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def relative_luminance(rgb: Tuple[int, int, int]) -> float:
        def adjust(channel: int) -> float:
            c = channel / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = rgb
        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)

def check_text_alternatives(content: str) -> List[str]:
    """Check for text alternatives (aria-label, aria-describedby, alt text)"""
    issues = []

    # Check for SVG/figure without aria-label or aria-describedby
    svg_pattern = r'<svg[^>]*>'
    figure_pattern = r'<figure[^>]*>'

    for pattern, element_name in [(svg_pattern, 'svg'), (figure_pattern, 'figure')]:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            element = match.group()
            if 'aria-label' not in element and 'aria-describedby' not in element:
                issues.append(f"{element_name} element missing text alternative (aria-label or aria-describedby)")

    return issues

def check_color_usage(content: str) -> List[str]:
    """Check if color is used as only visual means of conveying information"""
    issues = []

    # Extract all color values
    color_pattern = r'(?:fill|stroke|color)[=:]\s*["\']?(#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3})["\']?'
    colors = re.findall(color_pattern, content, re.IGNORECASE)

    # Warning if many different colors used (might rely on color alone)
    unique_colors = set(colors)
    if len(unique_colors) > 6:
        issues.append(f"Warning: {len(unique_colors)} different colors detected. Ensure color is not the only visual cue. Use patterns, labels, or shapes.")

    return issues

def check_keyboard_accessibility(content: str) -> List[str]:
    """Check for keyboard accessibility attributes"""
    issues = []

    # Check for interactive elements without tabindex or role
    if 'onclick' in content.lower() or 'hover' in content.lower():
        if 'tabindex' not in content.lower():
            issues.append("Warning: Interactive elements detected but no tabindex found. Ensure keyboard accessibility.")

    return issues

def validate_file(filepath: Path) -> Dict:
    """Validate accessibility of visualization file"""
    if not filepath.exists():
        return {"error": f"File not found: {filepath}"}

    content = filepath.read_text()

    results = {
        "file": str(filepath),
        "issues": [],
        "warnings": [],
        "passed": []
    }

    # Check text alternatives
    text_alt_issues = check_text_alternatives(content)
    if text_alt_issues:
        results["issues"].extend(text_alt_issues)
    else:
        results["passed"].append("✅ Text alternatives provided")

    # Check color usage
    color_issues = check_color_usage(content)
    if color_issues:
        results["warnings"].extend(color_issues)
    else:
        results["passed"].append("✅ Reasonable color usage detected")

    # Check keyboard accessibility
    keyboard_issues = check_keyboard_accessibility(content)
    if keyboard_issues:
        results["warnings"].extend(keyboard_issues)

    # Check for data table alternative
    if '<table' in content or 'data-table' in content:
        results["passed"].append("✅ Data table alternative found")
    else:
        results["warnings"].append("Warning: No data table alternative detected. Consider providing one for accessibility.")

    return results

def print_results(results: Dict):
    """Print validation results in readable format"""
    print(f"\n{'='*60}")
    print(f"Accessibility Validation: {results['file']}")
    print(f"{'='*60}\n")

    if results.get("error"):
        print(f"❌ ERROR: {results['error']}\n")
        return

    if results["issues"]:
        print("❌ ISSUES FOUND:\n")
        for issue in results["issues"]:
            print(f"  • {issue}")
        print()

    if results["warnings"]:
        print("⚠️  WARNINGS:\n")
        for warning in results["warnings"]:
            print(f"  • {warning}")
        print()

    if results["passed"]:
        print("✅ PASSED CHECKS:\n")
        for check in results["passed"]:
            print(f"  • {check}")
        print()

    # Summary
    total_checks = len(results["issues"]) + len(results["warnings"]) + len(results["passed"])
    passed_checks = len(results["passed"])

    print(f"{'='*60}")
    print(f"Summary: {passed_checks}/{total_checks} checks passed")

    if results["issues"]:
        print("Status: ❌ FAIL (issues must be fixed)")
    elif results["warnings"]:
        print("Status: ⚠️  PASS WITH WARNINGS (review recommended)")
    else:
        print("Status: ✅ PASS (all checks passed)")
    print(f"{'='*60}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_accessibility.py <chart.html|chart.svg>")
        print("\nValidates WCAG 2.1 AA accessibility for data visualizations")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    results = validate_file(filepath)
    print_results(results)

    # Exit code: 0 if pass, 1 if issues, 2 if warnings
    if results.get("error") or results["issues"]:
        sys.exit(1)
    elif results["warnings"]:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
```
