#!/usr/bin/env python3
"""
Validate Form Data Against Schema

Tests form data against JSON Schema validation rules.

Usage:
    python validate_form_data.py --schema schema.json --data form-data.json
    python validate_form_data.py --schema contact-form.json --data test-data.json
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, List

def validate_string(value: Any, rules: Dict) -> List[str]:
    """Validate string value"""
    errors = []

    if not isinstance(value, str):
        errors.append(f"Expected string, got {type(value).__name__}")
        return errors

    if 'minLength' in rules and len(value) < rules['minLength']:
        errors.append(f"Minimum length {rules['minLength']}, got {len(value)}")

    if 'maxLength' in rules and len(value) > rules['maxLength']:
        errors.append(f"Maximum length {rules['maxLength']}, got {len(value)}")

    if 'pattern' in rules:
        import re
        if not re.match(rules['pattern'], value):
            errors.append(f"Does not match pattern: {rules['pattern']}")

    if 'format' in rules:
        if rules['format'] == 'email':
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                errors.append("Invalid email format")

    if 'enum' in rules and value not in rules['enum']:
        errors.append(f"Value must be one of: {', '.join(rules['enum'])}")

    return errors

def validate_number(value: Any, rules: Dict) -> List[str]:
    """Validate number value"""
    errors = []

    if not isinstance(value, (int, float)):
        errors.append(f"Expected number, got {type(value).__name__}")
        return errors

    if 'minimum' in rules and value < rules['minimum']:
        errors.append(f"Minimum value {rules['minimum']}, got {value}")

    if 'maximum' in rules and value > rules['maximum']:
        errors.append(f"Maximum value {rules['maximum']}, got {value}")

    if rules.get('type') == 'integer' and not isinstance(value, int):
        errors.append(f"Expected integer, got float")

    return errors

def validate_field(field_name: str, value: Any, rules: Dict) -> List[str]:
    """Validate single field"""
    field_type = rules.get('type', 'string')

    if field_type == 'string':
        return validate_string(value, rules)
    elif field_type in ['number', 'integer']:
        return validate_number(value, rules)
    elif field_type == 'boolean':
        if not isinstance(value, bool):
            return [f"Expected boolean, got {type(value).__name__}"]
    elif field_type == 'array':
        if not isinstance(value, list):
            return [f"Expected array, got {type(value).__name__}"]
    elif field_type == 'object':
        if not isinstance(value, dict):
            return [f"Expected object, got {type(value).__name__}"]

    return []

def validate_data(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict:
    """Validate data against schema"""
    results = {
        "valid": True,
        "errors": {},
        "missing_required": []
    }

    # Check required fields
    required_fields = schema.get('required', [])
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            results["missing_required"].append(field)
            results["valid"] = False

    # Validate each field
    properties = schema.get('properties', {})
    for field_name, value in data.items():
        if field_name in properties:
            field_errors = validate_field(field_name, value, properties[field_name])
            if field_errors:
                results["errors"][field_name] = field_errors
                results["valid"] = False

    return results

def print_validation_results(results: Dict):
    """Print validation results"""
    print(f"\n{'='*70}")
    print("Form Data Validation Results")
    print(f"{'='*70}\n")

    if results["valid"]:
        print("✅ ALL VALIDATION PASSED\n")
        print(f"{'='*70}")
        return

    if results["missing_required"]:
        print("❌ MISSING REQUIRED FIELDS:\n")
        for field in results["missing_required"]:
            print(f"  • {field}")
        print()

    if results["errors"]:
        print("❌ VALIDATION ERRORS:\n")
        for field, errors in results["errors"].items():
            print(f"  {field}:")
            for error in errors:
                print(f"    - {error}")
        print()

    print(f"{'='*70}")
    print("Status: ❌ VALIDATION FAILED")
    print(f"{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(description='Validate form data against JSON Schema')
    parser.add_argument('--schema', type=str, required=True, help='JSON Schema file')
    parser.add_argument('--data', type=str, required=True, help='Form data JSON file')

    args = parser.parse_args()

    # Load schema
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"❌ Error: Schema file not found: {schema_path}")
        sys.exit(1)

    schema = json.loads(schema_path.read_text())
    print(f"✅ Loaded schema from {schema_path}")

    # Load data
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"❌ Error: Data file not found: {data_path}")
        sys.exit(1)

    data = json.loads(data_path.read_text())
    print(f"✅ Loaded data from {data_path}")

    # Validate
    results = validate_data(data, schema)
    print_validation_results(results)

    sys.exit(0 if results["valid"] else 1)

if __name__ == "__main__":
    main()
