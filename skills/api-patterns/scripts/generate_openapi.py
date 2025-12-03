#!/usr/bin/env python3
"""
Generate OpenAPI spec from FastAPI application

Usage:
    python generate_openapi.py path/to/app.py output.json

Extracts OpenAPI specification without running the server.
"""

import sys
import json
from pathlib import Path
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec


def load_fastapi_app(file_path: str, app_name: str = "app"):
    """Load FastAPI app from Python file"""
    file_path = Path(file_path).resolve()

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    # Load module from file
    spec = spec_from_file_location("app_module", file_path)
    if spec is None or spec.loader is None:
        print(f"Error: Could not load module from {file_path}")
        sys.exit(1)

    module = module_from_spec(spec)
    sys.modules["app_module"] = module
    spec.loader.exec_module(module)

    # Get FastAPI app
    if not hasattr(module, app_name):
        print(f"Error: No '{app_name}' found in {file_path}")
        print(f"Available attributes: {dir(module)}")
        sys.exit(1)

    app = getattr(module, app_name)

    # Verify it's a FastAPI app
    try:
        from fastapi import FastAPI
        if not isinstance(app, FastAPI):
            print(f"Error: '{app_name}' is not a FastAPI instance")
            sys.exit(1)
    except ImportError:
        print("Error: FastAPI not installed")
        sys.exit(1)

    return app


def generate_openapi_spec(app, output_path: str, format: str = "json"):
    """Generate OpenAPI spec from FastAPI app"""
    openapi_schema = app.openapi()

    output_path = Path(output_path)

    if format == "json":
        with open(output_path, "w") as f:
            json.dump(openapi_schema, f, indent=2)
        print(f"✓ OpenAPI spec generated: {output_path}")
        print(f"  Title: {openapi_schema['info']['title']}")
        print(f"  Version: {openapi_schema['info']['version']}")
        print(f"  Endpoints: {len(openapi_schema['paths'])}")
    elif format == "yaml":
        try:
            import yaml
            with open(output_path, "w") as f:
                yaml.dump(openapi_schema, f, sort_keys=False)
            print(f"✓ OpenAPI spec generated: {output_path}")
        except ImportError:
            print("Error: PyYAML not installed. Install with: pip install pyyaml")
            sys.exit(1)
    else:
        print(f"Error: Unknown format '{format}'. Use 'json' or 'yaml'")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_openapi.py <app_file.py> <output.json>")
        print("")
        print("Examples:")
        print("  python generate_openapi.py main.py openapi.json")
        print("  python generate_openapi.py app/main.py:application spec.yaml")
        print("")
        print("Arguments:")
        print("  app_file.py   - Python file containing FastAPI app")
        print("  output.json   - Output file (.json or .yaml)")
        print("")
        print("Optional:")
        print("  Use 'file.py:varname' to specify app variable name (default: 'app')")
        sys.exit(1)

    app_arg = sys.argv[1]
    output_file = sys.argv[2]

    # Parse app file and variable name
    if ":" in app_arg:
        app_file, app_name = app_arg.split(":", 1)
    else:
        app_file = app_arg
        app_name = "app"

    # Determine format from output file extension
    output_path = Path(output_file)
    if output_path.suffix == ".yaml" or output_path.suffix == ".yml":
        format = "yaml"
    else:
        format = "json"

    # Load FastAPI app
    print(f"Loading FastAPI app from {app_file}...")
    app = load_fastapi_app(app_file, app_name)

    # Generate OpenAPI spec
    print(f"Generating OpenAPI spec...")
    generate_openapi_spec(app, output_file, format)


if __name__ == "__main__":
    main()
