#!/usr/bin/env python3
"""
Generate route configurations for Flask, Django, or FastAPI from a YAML config file.

Usage:
    python generate_routes.py --framework flask --config routes.yaml
    python generate_routes.py --framework django --config routes.yaml --output urls.py
    python generate_routes.py --framework fastapi --config routes.yaml
"""

import argparse
import yaml
import sys
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime


def load_config(config_path: str) -> Dict[str, Any]:
    """Load route configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)


def generate_flask_routes(config: Dict[str, Any]) -> str:
    """Generate Flask route code."""
    output = []
    output.append('"""')
    output.append(f'Generated Flask routes - {datetime.now().isoformat()}')
    output.append('"""')
    output.append('from flask import Blueprint, render_template, request, jsonify')
    output.append('from flask_login import login_required\n')

    # Group routes by blueprint
    blueprints = {}
    for route in config.get('routes', []):
        bp_name = route.get('blueprint', 'main')
        if bp_name not in blueprints:
            blueprints[bp_name] = []
        blueprints[bp_name].append(route)

    # Generate blueprint code
    for bp_name, routes in blueprints.items():
        if bp_name != 'main':
            output.append(f"\n# {bp_name.title()} Blueprint")
            output.append(f"{bp_name}_bp = Blueprint('{bp_name}', __name__, url_prefix='/{bp_name}')\n")

        for route in routes:
            # Generate route decorator
            methods = route.get('methods', ['GET'])
            methods_str = str(methods) if len(methods) > 1 else ''

            if bp_name != 'main':
                decorator = f"@{bp_name}_bp.route('{route['path']}'"
            else:
                decorator = f"@app.route('{route['path']}'"

            if methods_str:
                decorator += f", methods={methods_str}"
            decorator += ")"

            output.append(decorator)

            # Add authentication decorator if required
            if route.get('auth_required', False):
                output.append('@login_required')

            # Add role decorator if specified
            if 'roles' in route:
                roles_str = ', '.join([f"'{role}'" for role in route['roles']])
                output.append(f'@require_roles({roles_str})')

            # Generate function
            func_name = route.get('name', route['path'].replace('/', '_').strip('_'))
            params = extract_params(route['path'])
            param_str = ', '.join(params) if params else ''

            output.append(f"def {func_name}({param_str}):")
            output.append(f'    """{route.get("description", "Route handler")}"""')

            # Generate function body
            if route.get('template'):
                output.append(f"    return render_template('{route['template']}')")
            elif 'api' in route and route['api']:
                output.append('    # API endpoint')
                output.append('    data = {}  # Fetch data')
                output.append('    return jsonify(data)')
            else:
                output.append('    # Implement route logic')
                output.append('    pass')

            output.append('')

    return '\n'.join(output)


def generate_django_routes(config: Dict[str, Any]) -> str:
    """Generate Django URL patterns."""
    output = []
    output.append('"""')
    output.append(f'Generated Django URL patterns - {datetime.now().isoformat()}')
    output.append('"""')
    output.append('from django.urls import path, include')
    output.append('from . import views\n')
    output.append("app_name = 'main'\n")
    output.append('urlpatterns = [')

    for route in config.get('routes', []):
        path_str = convert_to_django_path(route['path'])
        view_name = route.get('view', route.get('name', 'view_' + route['path'].replace('/', '_').strip('_')))
        name = route.get('name', route['path'].replace('/', '_').strip('_'))

        # Generate path pattern
        if route.get('class_based', False):
            output.append(f"    path('{path_str}', views.{view_name}.as_view(), name='{name}'),")
        else:
            output.append(f"    path('{path_str}', views.{view_name}, name='{name}'),")

    output.append(']')

    # Generate view stubs
    output.append('\n# View stubs (implement in views.py):')
    output.append('# from django.shortcuts import render')
    output.append('# from django.views.generic import ListView, DetailView\n')

    for route in config.get('routes', []):
        view_name = route.get('view', route.get('name', 'view_' + route['path'].replace('/', '_').strip('_')))
        if route.get('class_based', False):
            output.append(f"# class {view_name}(ListView):")
            output.append(f"#     model = None  # Set your model")
            output.append(f"#     template_name = '{route.get('template', 'template.html')}'")
        else:
            output.append(f"# def {view_name}(request):")
            output.append(f"#     return render(request, '{route.get('template', 'template.html')}')")
        output.append('')

    return '\n'.join(output)


def generate_fastapi_routes(config: Dict[str, Any]) -> str:
    """Generate FastAPI route code."""
    output = []
    output.append('"""')
    output.append(f'Generated FastAPI routes - {datetime.now().isoformat()}')
    output.append('"""')
    output.append('from fastapi import APIRouter, Depends, HTTPException, Query, Path')
    output.append('from pydantic import BaseModel')
    output.append('from typing import Optional, List\n')

    # Group routes by router
    routers = {}
    for route in config.get('routes', []):
        router_name = route.get('router', 'main')
        if router_name not in routers:
            routers[router_name] = []
        routers[router_name].append(route)

    # Generate router code
    for router_name, routes in routers.items():
        output.append(f"# {router_name.title()} Router")
        output.append(f"{router_name}_router = APIRouter(")

        if router_name != 'main':
            output.append(f"    prefix='/{router_name}',")
            output.append(f"    tags=['{router_name}']")

        output.append(')\n')

        for route in routes:
            # Generate route decorator
            method = route.get('method', 'get').lower()
            path = convert_to_fastapi_path(route['path'])

            # Response model if specified
            response_model = ''
            if route.get('response_model'):
                response_model = f", response_model={route['response_model']}"

            output.append(f"@{router_name}_router.{method}('{path}'{response_model})")

            # Generate function
            func_name = route.get('name', route['path'].replace('/', '_').strip('_'))
            params = generate_fastapi_params(route)

            output.append(f"async def {func_name}({params}):")
            output.append(f'    """{route.get("description", "Route handler")}"""')

            # Generate function body
            if route.get('response'):
                output.append(f"    return {route['response']}")
            else:
                output.append('    # Implement route logic')
                output.append('    return {"message": "Not implemented"}')

            output.append('')

    # Generate models if specified
    if 'models' in config:
        output.append('# Pydantic Models')
        for model in config['models']:
            output.append(f"class {model['name']}(BaseModel):")
            for field in model.get('fields', []):
                field_type = field.get('type', 'str')
                optional = 'Optional[' if field.get('optional', False) else ''
                optional_close = ']' if field.get('optional', False) else ''
                default = ' = None' if field.get('optional', False) else ''
                output.append(f"    {field['name']}: {optional}{field_type}{optional_close}{default}")
            output.append('')

    return '\n'.join(output)


def extract_params(path: str) -> List[str]:
    """Extract parameters from Flask-style path."""
    import re
    params = re.findall(r'<(?:\w+:)?(\w+)>', path)
    return params


def convert_to_django_path(path: str) -> str:
    """Convert Flask-style path to Django path."""
    import re
    # Convert <type:name> to <type:name>
    path = re.sub(r'<int:(\w+)>', r'<int:\1>', path)
    path = re.sub(r'<string:(\w+)>', r'<str:\1>', path)
    path = re.sub(r'<(\w+)>', r'<str:\1>', path)  # Default to str
    return path.lstrip('/')


def convert_to_fastapi_path(path: str) -> str:
    """Convert Flask-style path to FastAPI path."""
    import re
    # Convert <type:name> to {name}
    path = re.sub(r'<(?:\w+:)?(\w+)>', r'{\1}', path)
    return path


def generate_fastapi_params(route: Dict[str, Any]) -> str:
    """Generate FastAPI function parameters."""
    params = []

    # Extract path parameters
    import re
    path_params = re.findall(r'<(?:\w+:)?(\w+)>', route['path'])
    for param in path_params:
        param_type = 'str'  # Default type
        if '<int:' in route['path']:
            param_type = 'int'
        params.append(f"{param}: {param_type} = Path(...)")

    # Add query parameters if specified
    for query_param in route.get('query_params', []):
        param_name = query_param['name']
        param_type = query_param.get('type', 'str')
        required = query_param.get('required', False)
        default = '...' if required else 'None'
        optional = '' if required else 'Optional'

        if optional:
            params.append(f"{param_name}: {optional}[{param_type}] = Query({default})")
        else:
            params.append(f"{param_name}: {param_type} = Query({default})")

    # Add request body if specified
    if route.get('body'):
        params.append(f"body: {route['body']}")

    # Add dependencies if specified
    for dep in route.get('dependencies', []):
        params.append(f"{dep['name']} = Depends({dep['function']})")

    return ', '.join(params) if params else ''


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate route configuration."""
    if 'routes' not in config:
        print("Error: 'routes' key not found in config")
        return False

    for i, route in enumerate(config['routes']):
        if 'path' not in route:
            print(f"Error: Route {i} missing 'path'")
            return False

        # Check for duplicate paths
        paths = [r['path'] for r in config['routes']]
        if len(paths) != len(set(paths)):
            print("Warning: Duplicate paths detected")

    return True


def main():
    parser = argparse.ArgumentParser(description='Generate route configurations for Python web frameworks')
    parser.add_argument('--framework', choices=['flask', 'django', 'fastapi'], required=True,
                        help='Target framework')
    parser.add_argument('--config', required=True, help='Path to YAML configuration file')
    parser.add_argument('--output', help='Output file path (default: stdout)')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Validate configuration
    if not validate_config(config):
        sys.exit(1)

    # Generate routes based on framework
    if args.framework == 'flask':
        output = generate_flask_routes(config)
    elif args.framework == 'django':
        output = generate_django_routes(config)
    elif args.framework == 'fastapi':
        output = generate_fastapi_routes(config)
    else:
        print(f"Error: Unknown framework '{args.framework}'")
        sys.exit(1)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Routes generated successfully: {args.output}")
    else:
        print(output)


# Example YAML configuration format:
"""
routes:
  - path: /
    name: index
    methods: [GET]
    template: index.html
    description: Home page

  - path: /api/products
    name: get_products
    method: GET
    router: api
    response_model: List[Product]
    query_params:
      - name: category
        type: str
        required: false
    description: Get all products

  - path: /products/<int:product_id>
    name: product_detail
    methods: [GET]
    template: product.html
    auth_required: true
    description: Product detail page

models:
  - name: Product
    fields:
      - name: id
        type: int
      - name: name
        type: str
      - name: price
        type: float
      - name: description
        type: str
        optional: true
"""

if __name__ == '__main__':
    main()