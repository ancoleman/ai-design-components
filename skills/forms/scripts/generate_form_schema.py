#!/usr/bin/env python3
"""
Generate JSON Schema from Form Configuration

Creates JSON Schema for form validation from YAML/JSON configuration.

Usage:
    python generate_form_schema.py --input form-config.yaml --output schema.json
    python generate_form_schema.py --type contact-form
"""

import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, Any

# Common field type mappings
FIELD_TYPE_MAP = {
    'text': {'type': 'string'},
    'email': {'type': 'string', 'format': 'email'},
    'password': {'type': 'string', 'minLength': 8},
    'number': {'type': 'number'},
    'integer': {'type': 'integer'},
    'boolean': {'type': 'boolean'},
    'date': {'type': 'string', 'format': 'date'},
    'datetime': {'type': 'string', 'format': 'date-time'},
    'url': {'type': 'string', 'format': 'uri'},
    'tel': {'type': 'string', 'pattern': '^[+]?[(]?[0-9]{1,4}[)]?[-\\s\\.]?[(]?[0-9]{1,4}[)]?[-\\s\\.]?[0-9]{1,9}$'},
}

def create_field_schema(field_config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert field configuration to JSON Schema property"""
    field_type = field_config.get('type', 'text')
    schema = FIELD_TYPE_MAP.get(field_type, {'type': 'string'}).copy()

    # Add constraints
    if 'minLength' in field_config:
        schema['minLength'] = field_config['minLength']
    if 'maxLength' in field_config:
        schema['maxLength'] = field_config['maxLength']
    if 'minimum' in field_config:
        schema['minimum'] = field_config['minimum']
    if 'maximum' in field_config:
        schema['maximum'] = field_config['maximum']
    if 'pattern' in field_config:
        schema['pattern'] = field_config['pattern']
    if 'enum' in field_config:
        schema['enum'] = field_config['enum']

    # Add metadata
    if 'title' in field_config:
        schema['title'] = field_config['title']
    if 'description' in field_config:
        schema['description'] = field_config['description']
    if 'default' in field_config:
        schema['default'] = field_config['default']

    return schema

def generate_schema(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate complete JSON Schema from form configuration"""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": config.get('title', 'Form'),
        "description": config.get('description', ''),
        "properties": {},
        "required": []
    }

    # Process fields
    for field_name, field_config in config.get('fields', {}).items():
        schema['properties'][field_name] = create_field_schema(field_config)

        if field_config.get('required', False):
            schema['required'].append(field_name)

    # Additional validation
    if 'additionalProperties' in config:
        schema['additionalProperties'] = config['additionalProperties']

    return schema

# Predefined form templates
FORM_TEMPLATES = {
    'contact-form': {
        'title': 'Contact Form',
        'description': 'Basic contact form schema',
        'fields': {
            'name': {
                'type': 'text',
                'title': 'Full Name',
                'minLength': 2,
                'maxLength': 100,
                'required': True
            },
            'email': {
                'type': 'email',
                'title': 'Email Address',
                'required': True
            },
            'subject': {
                'type': 'text',
                'title': 'Subject',
                'minLength': 5,
                'maxLength': 200,
                'required': True
            },
            'message': {
                'type': 'text',
                'title': 'Message',
                'minLength': 20,
                'maxLength': 2000,
                'required': True
            },
            'newsletter': {
                'type': 'boolean',
                'title': 'Subscribe to Newsletter',
                'default': False,
                'required': False
            }
        }
    },
    'registration-form': {
        'title': 'User Registration',
        'description': 'User registration form schema',
        'fields': {
            'username': {
                'type': 'text',
                'title': 'Username',
                'minLength': 3,
                'maxLength': 20,
                'pattern': '^[a-zA-Z0-9_-]+$',
                'required': True
            },
            'email': {
                'type': 'email',
                'title': 'Email',
                'required': True
            },
            'password': {
                'type': 'password',
                'title': 'Password',
                'minLength': 8,
                'maxLength': 100,
                'required': True
            },
            'confirmPassword': {
                'type': 'password',
                'title': 'Confirm Password',
                'required': True
            },
            'age': {
                'type': 'integer',
                'title': 'Age',
                'minimum': 13,
                'maximum': 120,
                'required': True
            },
            'terms': {
                'type': 'boolean',
                'title': 'Agree to Terms',
                'required': True
            }
        }
    }
}

def main():
    parser = argparse.ArgumentParser(description='Generate JSON Schema from form configuration')
    parser.add_argument('--input', type=str, help='Input YAML/JSON configuration file')
    parser.add_argument('--output', type=str, help='Output JSON Schema file')
    parser.add_argument('--type', choices=list(FORM_TEMPLATES.keys()),
                       help='Use predefined form template')

    args = parser.parse_args()

    # Load configuration
    if args.type:
        config = FORM_TEMPLATES[args.type]
        print(f"✅ Using predefined template: {args.type}")
    elif args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Error: File not found: {input_path}")
            sys.exit(1)

        content = input_path.read_text()
        if input_path.suffix == '.yaml' or input_path.suffix == '.yml':
            config = yaml.safe_load(content)
        else:
            config = json.loads(content)
        print(f"✅ Loaded configuration from {input_path}")
    else:
        print("❌ Error: Either --input or --type required")
        sys.exit(1)

    # Generate schema
    schema = generate_schema(config)
    schema_json = json.dumps(schema, indent=2)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(schema_json)
        print(f"✅ Schema saved to {output_path}")
    else:
        print("\nGenerated JSON Schema:")
        print(schema_json)

if __name__ == "__main__":
    main()
