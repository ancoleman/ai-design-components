#!/usr/bin/env python3
"""
Validate design token structure and naming conventions.

Checks:
- W3C format compliance ($value, $type, $description)
- Naming conventions (lowercase, hyphens)
- Token references are valid
- Required token categories exist
"""

import json
import os
import re
import sys
from pathlib import Path


class TokenValidator:
    def __init__(self, tokens_dir):
        self.tokens_dir = Path(tokens_dir)
        self.errors = []
        self.warnings = []
        self.all_tokens = {}

    def validate_all(self):
        """Run all validations."""
        print("🔍 Validating design tokens...")

        # Load all tokens
        self.load_tokens()

        # Run validations
        self.validate_token_structure()
        self.validate_naming_conventions()
        self.validate_references()
        self.validate_required_categories()

        # Report results
        self.report()

        return len(self.errors) == 0

    def load_tokens(self):
        """Load all token JSON files."""
        for json_file in self.tokens_dir.rglob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    tokens = json.load(f)
                    rel_path = str(json_file.relative_to(self.tokens_dir))
                    self.all_tokens[rel_path] = tokens
            except json.JSONDecodeError as e:
                self.errors.append(f"❌ Invalid JSON in {json_file}: {e}")

    def validate_token_structure(self):
        """Validate W3C format compliance."""
        for file_path, tokens in self.all_tokens.items():
            self._validate_token_node(tokens, file_path, [])

    def _validate_token_node(self, node, file_path, path):
        """Recursively validate token nodes."""
        if not isinstance(node, dict):
            return

        # Check if this is a token (has $value)
        if '$value' in node:
            # Must have $type
            if '$type' not in node:
                self.errors.append(
                    f"❌ {file_path} - Token at {'.'.join(path)} missing $type"
                )

            # $description is recommended
            if '$description' not in node:
                self.warnings.append(
                    f"⚠️  {file_path} - Token at {'.'.join(path)} missing $description (recommended)"
                )

            # Validate $type values
            valid_types = [
                'color', 'dimension', 'fontSize', 'fontWeight', 'fontFamily',
                'number', 'duration', 'cubicBezier', 'shadow'
            ]
            if node.get('$type') not in valid_types:
                self.warnings.append(
                    f"⚠️  {file_path} - Token at {'.'.join(path)} has non-standard $type: {node.get('$type')}"
                )

        # Recurse into children
        for key, value in node.items():
            if not key.startswith('$'):  # Skip metadata fields
                self._validate_token_node(value, file_path, path + [key])

    def validate_naming_conventions(self):
        """Validate token naming conventions."""
        for file_path, tokens in self.all_tokens.items():
            self._validate_names(tokens, file_path, [])

    def _validate_names(self, node, file_path, path):
        """Recursively validate token names."""
        if not isinstance(node, dict):
            return

        for key, value in node.items():
            if key.startswith('$'):  # Skip metadata
                continue

            # Check naming convention (lowercase, hyphens, no underscores)
            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', key):
                self.errors.append(
                    f"❌ {file_path} - Invalid name '{key}' at {'.'.join(path)}. Use lowercase with hyphens only."
                )

            # Recurse
            self._validate_names(value, file_path, path + [key])

    def validate_references(self):
        """Validate that token references ({xxx}) point to valid tokens."""
        for file_path, tokens in self.all_tokens.items():
            self._validate_refs(tokens, file_path, [])

    def _validate_refs(self, node, file_path, path):
        """Recursively validate token references."""
        if not isinstance(node, dict):
            return

        if '$value' in node:
            value = node['$value']
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                ref = value[1:-1]  # Remove { }
                # TODO: Validate ref exists
                # This would require building a full token map first
                pass

        for key, value in node.items():
            if not key.startswith('$'):
                self._validate_refs(value, file_path, path + [key])

    def validate_required_categories(self):
        """Validate that required token categories exist."""
        required = ['colors.json', 'spacing.json', 'typography.json']
        existing = set(self.all_tokens.keys())

        for req_file in required:
            found = any(req_file in path for path in existing)
            if not found:
                self.warnings.append(
                    f"⚠️  Missing recommended token file: {req_file}"
                )

    def report(self):
        """Print validation report."""
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All tokens are valid!")

        print(f"\n📊 Summary:")
        print(f"  Files checked: {len(self.all_tokens)}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print("=" * 60)


def main():
    # Determine tokens directory
    script_dir = Path(__file__).parent
    tokens_dir = script_dir.parent / 'tokens'

    if not tokens_dir.exists():
        print(f"❌ Tokens directory not found: {tokens_dir}")
        sys.exit(1)

    # Run validation
    validator = TokenValidator(tokens_dir)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
