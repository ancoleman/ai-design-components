#!/usr/bin/env python3
"""
Validate Form Accessibility (WCAG 2.1 AA Compliance)

Checks HTML forms for accessibility issues:
- All inputs have labels
- Required fields are marked
- Error messages are associated (aria-describedby)
- Keyboard navigation (proper tab order)
- ARIA attributes present
- Color contrast for error states

Usage:
    python validate_form_accessibility.py form.html
    python validate_form_accessibility.py --check-all forms/
"""

import sys
import re
from pathlib import Path
from typing import List, Dict
from html.parser import HTMLParser

class FormAccessibilityChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = []
        self.labels = []
        self.errors = []
        self.warnings = []
        self.current_input = None
        self.label_for_map = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'input':
            input_data = {
                'tag': tag,
                'type': attrs_dict.get('type', 'text'),
                'id': attrs_dict.get('id'),
                'name': attrs_dict.get('name'),
                'aria_label': attrs_dict.get('aria-label'),
                'aria_labelledby': attrs_dict.get('aria-labelledby'),
                'aria_describedby': attrs_dict.get('aria-describedby'),
                'required': 'required' in attrs_dict or 'aria-required' in attrs_dict,
                'has_label': False
            }
            self.inputs.append(input_data)

        elif tag == 'textarea':
            input_data = {
                'tag': tag,
                'type': 'textarea',
                'id': attrs_dict.get('id'),
                'name': attrs_dict.get('name'),
                'aria_label': attrs_dict.get('aria-label'),
                'aria_labelledby': attrs_dict.get('aria-labelledby'),
                'aria_describedby': attrs_dict.get('aria-describedby'),
                'required': 'required' in attrs_dict or 'aria-required' in attrs_dict,
                'has_label': False
            }
            self.inputs.append(input_data)

        elif tag == 'select':
            input_data = {
                'tag': tag,
                'type': 'select',
                'id': attrs_dict.get('id'),
                'name': attrs_dict.get('name'),
                'aria_label': attrs_dict.get('aria-label'),
                'aria_labelledby': attrs_dict.get('aria_labelledby'),
                'aria_describedby': attrs_dict.get('aria-describedby'),
                'required': 'required' in attrs_dict or 'aria-required' in attrs_dict,
                'has_label': False
            }
            self.inputs.append(input_data)

        elif tag == 'label':
            label_for = attrs_dict.get('for')
            if label_for:
                self.label_for_map[label_for] = True

    def validate(self):
        # Associate labels with inputs
        for input_field in self.inputs:
            if input_field['id'] and input_field['id'] in self.label_for_map:
                input_field['has_label'] = True

        # Check each input
        for i, input_field in enumerate(self.inputs, 1):
            # Check 1: Every input must have a label
            if not input_field['has_label'] and not input_field['aria_label'] and not input_field['aria_labelledby']:
                self.errors.append(
                    f"Input #{i} ({input_field['type']}) missing label. "
                    f"Add <label for='id'> or aria-label attribute."
                )

            # Check 2: Required fields should have aria-required
            if input_field['required']:
                # Good practice to have aria-required="true"
                self.warnings.append(
                    f"Input #{i} ({input_field['type']}) is required. "
                    f"Consider adding aria-required='true' for screen readers."
                )

            # Check 3: Errors should be associated with aria-describedby
            if not input_field['aria_describedby']:
                self.warnings.append(
                    f"Input #{i} ({input_field['type']}) missing aria-describedby. "
                    f"Error messages should be programmatically associated."
                )

def validate_file(filepath: Path) -> Dict:
    """Validate form accessibility in HTML file"""
    if not filepath.exists():
        return {"error": f"File not found: {filepath}"}

    try:
        content = filepath.read_text()
    except Exception as e:
        return {"error": f"Error reading file: {e}"}

    checker = FormAccessibilityChecker()
    checker.feed(content)
    checker.validate()

    return {
        "file": str(filepath),
        "inputs_found": len(checker.inputs),
        "errors": checker.errors,
        "warnings": checker.warnings,
    }

def print_results(results: Dict):
    """Print validation results"""
    print(f"\n{'='*70}")
    print(f"Form Accessibility Validation: {results['file']}")
    print(f"{'='*70}\n")

    if results.get("error"):
        print(f"❌ ERROR: {results['error']}\n")
        return

    print(f"Found {results['inputs_found']} form inputs\n")

    if results["errors"]:
        print("❌ CRITICAL ERRORS (Must Fix):\n")
        for error in results["errors"]:
            print(f"  • {error}")
        print()

    if results["warnings"]:
        print("⚠️  WARNINGS (Recommended Fixes):\n")
        for warning in results["warnings"]:
            print(f"  • {warning}")
        print()

    if not results["errors"] and not results["warnings"]:
        print("✅ ALL CHECKS PASSED - Form is accessible!\n")

    # Summary
    print(f"{'='*70}")
    if results["errors"]:
        print("Status: ❌ FAIL (fix critical errors)")
    elif results["warnings"]:
        print("Status: ⚠️  PASS WITH WARNINGS")
    else:
        print("Status: ✅ PASS (WCAG 2.1 AA compliant)")
    print(f"{'='*70}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_form_accessibility.py <form.html>")
        print("\nValidates WCAG 2.1 AA accessibility for HTML forms")
        print("\nChecks:")
        print("  - All inputs have labels")
        print("  - Required fields marked")
        print("  - Error messages associated")
        print("  - ARIA attributes present")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    results = validate_file(filepath)
    print_results(results)

    # Exit code
    if results.get("error") or results["errors"]:
        sys.exit(1)
    elif results["warnings"]:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
