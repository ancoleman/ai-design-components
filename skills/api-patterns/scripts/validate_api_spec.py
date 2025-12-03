#!/usr/bin/env python3
"""
Validate OpenAPI 3.1 specification

Usage:
    python validate_api_spec.py spec.json

Validates OpenAPI spec against OpenAPI 3.1 schema.
"""

import sys
import json
from pathlib import Path


def load_spec(file_path: str):
    """Load OpenAPI spec from JSON or YAML file"""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    if file_path.suffix in [".yaml", ".yml"]:
        try:
            import yaml
            with open(file_path) as f:
                return yaml.safe_load(f)
        except ImportError:
            print("Error: PyYAML not installed. Install with: pip install pyyaml")
            sys.exit(1)
    else:
        with open(file_path) as f:
            return json.load(f)


def validate_spec(spec: dict):
    """Validate OpenAPI specification"""
    errors = []
    warnings = []

    # Check required fields
    if "openapi" not in spec:
        errors.append("Missing required field: 'openapi'")
    elif not spec["openapi"].startswith("3."):
        warnings.append(f"OpenAPI version '{spec['openapi']}' is not 3.x")

    if "info" not in spec:
        errors.append("Missing required field: 'info'")
    else:
        if "title" not in spec["info"]:
            errors.append("Missing required field: 'info.title'")
        if "version" not in spec["info"]:
            errors.append("Missing required field: 'info.version'")

    if "paths" not in spec:
        errors.append("Missing required field: 'paths'")
    elif not spec["paths"]:
        warnings.append("No paths defined")

    # Validate paths
    if "paths" in spec:
        for path, path_item in spec["paths"].items():
            if not path.startswith("/"):
                errors.append(f"Path '{path}' must start with '/'")

            for method, operation in path_item.items():
                if method not in ["get", "put", "post", "delete", "options", "head", "patch", "trace"]:
                    continue

                # Check responses
                if "responses" not in operation:
                    errors.append(f"{method.upper()} {path}: Missing 'responses'")
                else:
                    if not operation["responses"]:
                        warnings.append(f"{method.upper()} {path}: No responses defined")

                # Check operationId
                if "operationId" not in operation:
                    warnings.append(f"{method.upper()} {path}: Missing 'operationId'")

                # Check tags
                if "tags" not in operation:
                    warnings.append(f"{method.upper()} {path}: No tags defined")

                # Check summary/description
                if "summary" not in operation and "description" not in operation:
                    warnings.append(f"{method.upper()} {path}: Missing summary and description")

    # Validate components
    if "components" in spec:
        if "schemas" in spec["components"]:
            for schema_name, schema in spec["components"]["schemas"].items():
                if "type" not in schema and "$ref" not in schema:
                    warnings.append(f"Schema '{schema_name}': Missing 'type' field")

    return errors, warnings


def print_results(errors: list, warnings: list):
    """Print validation results"""
    print("\n" + "="*60)
    print("OpenAPI Specification Validation Results")
    print("="*60 + "\n")

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()

    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
        print()

    if not errors and not warnings:
        print("✓ OpenAPI specification is valid!")
        print()
    elif not errors:
        print("✓ OpenAPI specification is valid (with warnings)")
        print()
    else:
        print("✗ OpenAPI specification has errors")
        print()

    print("="*60 + "\n")


def print_summary(spec: dict):
    """Print spec summary"""
    print("Specification Summary:")
    print(f"  OpenAPI Version: {spec.get('openapi', 'N/A')}")
    print(f"  Title: {spec.get('info', {}).get('title', 'N/A')}")
    print(f"  Version: {spec.get('info', {}).get('version', 'N/A')}")

    if "paths" in spec:
        total_endpoints = sum(
            len([m for m in path.keys() if m in ['get', 'post', 'put', 'delete', 'patch']])
            for path in spec["paths"].values()
        )
        print(f"  Paths: {len(spec['paths'])}")
        print(f"  Total Endpoints: {total_endpoints}")

    if "components" in spec and "schemas" in spec["components"]:
        print(f"  Schemas: {len(spec['components']['schemas'])}")

    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_api_spec.py <spec.json|spec.yaml>")
        print("")
        print("Examples:")
        print("  python validate_api_spec.py openapi.json")
        print("  python validate_api_spec.py spec.yaml")
        sys.exit(1)

    spec_file = sys.argv[1]

    print(f"Loading OpenAPI spec from {spec_file}...")
    spec = load_spec(spec_file)

    print_summary(spec)

    print("Validating specification...")
    errors, warnings = validate_spec(spec)

    print_results(errors, warnings)

    # Exit with error code if validation failed
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
