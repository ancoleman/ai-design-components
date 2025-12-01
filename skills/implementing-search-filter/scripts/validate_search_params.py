#!/usr/bin/env python3
"""
Validate and sanitize search parameters to prevent injection attacks and ensure data integrity.

This script validates search inputs, filters, and pagination parameters
to ensure they meet security and business logic requirements.
"""

import re
import json
import argparse
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date


class SearchParamValidator:
    """Validate and sanitize search parameters."""

    # Define validation rules
    RULES = {
        'query': {
            'type': str,
            'min_length': 0,
            'max_length': 200,
            'pattern': r'^[a-zA-Z0-9\s\-\.\,\!\?\'\"\&]+$',  # Alphanumeric + common punctuation
            'sanitize': True
        },
        'categories': {
            'type': list,
            'max_items': 20,
            'item_type': str,
            'allowed_values': None  # Will be set in __init__ if needed
        },
        'brands': {
            'type': list,
            'max_items': 20,
            'item_type': str
        },
        'min_price': {
            'type': (int, float),
            'min_value': 0,
            'max_value': 1000000
        },
        'max_price': {
            'type': (int, float),
            'min_value': 0,
            'max_value': 1000000
        },
        'sort_by': {
            'type': str,
            'allowed_values': [
                'relevance', 'price_asc', 'price_desc',
                'newest', 'oldest', 'rating', 'popularity'
            ]
        },
        'page': {
            'type': int,
            'min_value': 1,
            'max_value': 100
        },
        'per_page': {
            'type': int,
            'min_value': 1,
            'max_value': 100,
            'default': 20
        },
        'in_stock': {
            'type': bool
        },
        'date_from': {
            'type': str,
            'date_format': '%Y-%m-%d'
        },
        'date_to': {
            'type': str,
            'date_format': '%Y-%m-%d'
        }
    }

    # SQL injection patterns to block
    SQL_INJECTION_PATTERNS = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
        r'(--|\/\*|\*\/|xp_|sp_|@@)',
        r'(\bunion\b.*\bselect\b)',
        r'(;.*\b(SELECT|INSERT|UPDATE|DELETE)\b)',
        r'(\bOR\b.*=.*)',
        r"('.*\bOR\b.*'=')",
    ]

    def __init__(self, allowed_categories: Optional[List[str]] = None):
        """Initialize validator with optional allowed categories."""
        if allowed_categories:
            self.RULES['categories']['allowed_values'] = allowed_categories

    def validate(self, params: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        Validate search parameters.

        Returns:
            Tuple of (is_valid, cleaned_params, error_messages)
        """
        cleaned = {}
        errors = []

        for param_name, param_value in params.items():
            if param_value is None:
                continue

            if param_name not in self.RULES:
                # Unknown parameter - skip but log warning
                errors.append(f"Unknown parameter: {param_name}")
                continue

            rule = self.RULES[param_name]
            result = self._validate_param(param_name, param_value, rule)

            if result['valid']:
                cleaned[param_name] = result['value']
            else:
                errors.extend(result['errors'])

        # Additional cross-field validation
        cross_errors = self._cross_validate(cleaned)
        errors.extend(cross_errors)

        # Apply defaults for missing required params
        cleaned = self._apply_defaults(cleaned)

        return len(errors) == 0, cleaned, errors

    def _validate_param(self, name: str, value: Any, rule: Dict) -> Dict:
        """Validate a single parameter."""
        result = {'valid': True, 'value': value, 'errors': []}

        # Type validation
        expected_type = rule.get('type')
        if expected_type and not isinstance(value, expected_type):
            result['valid'] = False
            result['errors'].append(
                f"{name}: Expected {expected_type.__name__}, got {type(value).__name__}"
            )
            return result

        # String validation
        if isinstance(value, str):
            validated = self._validate_string(name, value, rule)
            result.update(validated)

        # List validation
        elif isinstance(value, list):
            validated = self._validate_list(name, value, rule)
            result.update(validated)

        # Number validation
        elif isinstance(value, (int, float)):
            validated = self._validate_number(name, value, rule)
            result.update(validated)

        # Boolean validation
        elif isinstance(value, bool):
            result['value'] = value

        # Date validation
        if rule.get('date_format'):
            validated = self._validate_date(name, str(value), rule['date_format'])
            result.update(validated)

        return result

    def _validate_string(self, name: str, value: str, rule: Dict) -> Dict:
        """Validate string parameter."""
        result = {'valid': True, 'value': value, 'errors': []}

        # Check for SQL injection attempts
        for pattern in self.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                result['valid'] = False
                result['errors'].append(
                    f"{name}: Potential SQL injection detected"
                )
                return result

        # Length validation
        min_len = rule.get('min_length', 0)
        max_len = rule.get('max_length', float('inf'))

        if len(value) < min_len:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Must be at least {min_len} characters"
            )

        if len(value) > max_len:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Must be at most {max_len} characters"
            )

        # Pattern validation
        pattern = rule.get('pattern')
        if pattern and not re.match(pattern, value):
            result['valid'] = False
            result['errors'].append(
                f"{name}: Contains invalid characters"
            )

        # Allowed values validation
        allowed = rule.get('allowed_values')
        if allowed and value not in allowed:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Must be one of {allowed}"
            )

        # Sanitization
        if rule.get('sanitize') and result['valid']:
            result['value'] = self._sanitize_string(value)

        return result

    def _validate_list(self, name: str, value: List, rule: Dict) -> Dict:
        """Validate list parameter."""
        result = {'valid': True, 'value': value, 'errors': []}

        # Max items check
        max_items = rule.get('max_items', float('inf'))
        if len(value) > max_items:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Cannot have more than {max_items} items"
            )

        # Item type validation
        item_type = rule.get('item_type')
        if item_type:
            for i, item in enumerate(value):
                if not isinstance(item, item_type):
                    result['valid'] = False
                    result['errors'].append(
                        f"{name}[{i}]: Expected {item_type.__name__}"
                    )

        # Allowed values for items
        allowed = rule.get('allowed_values')
        if allowed:
            invalid_items = [item for item in value if item not in allowed]
            if invalid_items:
                result['valid'] = False
                result['errors'].append(
                    f"{name}: Invalid items: {invalid_items}"
                )

        # Sanitize string items
        if item_type == str and result['valid']:
            result['value'] = [self._sanitize_string(item) for item in value]

        return result

    def _validate_number(self, name: str, value: float, rule: Dict) -> Dict:
        """Validate numeric parameter."""
        result = {'valid': True, 'value': value, 'errors': []}

        min_val = rule.get('min_value', float('-inf'))
        max_val = rule.get('max_value', float('inf'))

        if value < min_val:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Must be at least {min_val}"
            )

        if value > max_val:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Must be at most {max_val}"
            )

        return result

    def _validate_date(self, name: str, value: str, date_format: str) -> Dict:
        """Validate date parameter."""
        result = {'valid': True, 'value': value, 'errors': []}

        try:
            parsed_date = datetime.strptime(value, date_format)
            result['value'] = parsed_date.strftime(date_format)

            # Check if date is not in future (for most cases)
            if parsed_date.date() > date.today():
                result['errors'].append(
                    f"{name}: Date cannot be in the future"
                )
        except ValueError:
            result['valid'] = False
            result['errors'].append(
                f"{name}: Invalid date format (expected {date_format})"
            )

        return result

    def _sanitize_string(self, value: str) -> str:
        """Sanitize string to prevent XSS and injection."""
        # Remove HTML tags
        value = re.sub(r'<[^>]+>', '', value)

        # Escape special characters
        value = value.replace('&', '&amp;')
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        value = value.replace('"', '&quot;')
        value = value.replace("'", '&#x27;')

        # Normalize whitespace
        value = ' '.join(value.split())

        return value.strip()

    def _cross_validate(self, params: Dict) -> List[str]:
        """Perform cross-field validation."""
        errors = []

        # Price range validation
        min_price = params.get('min_price')
        max_price = params.get('max_price')

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                errors.append("min_price cannot be greater than max_price")

        # Date range validation
        date_from = params.get('date_from')
        date_to = params.get('date_to')

        if date_from and date_to:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d')
                to_date = datetime.strptime(date_to, '%Y-%m-%d')

                if from_date > to_date:
                    errors.append("date_from cannot be after date_to")
            except ValueError:
                pass  # Already handled in individual validation

        return errors

    def _apply_defaults(self, params: Dict) -> Dict:
        """Apply default values for missing parameters."""
        defaults = {
            'page': 1,
            'per_page': 20,
            'sort_by': 'relevance'
        }

        for key, default_value in defaults.items():
            if key not in params:
                rule = self.RULES.get(key, {})
                if 'default' in rule:
                    params[key] = rule['default']
                elif key in defaults:
                    params[key] = default_value

        return params


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Validate search parameters'
    )

    parser.add_argument(
        '--params',
        type=str,
        required=True,
        help='JSON string of search parameters'
    )

    parser.add_argument(
        '--categories',
        type=str,
        help='Comma-separated list of allowed categories'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on any validation error'
    )

    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        print(f"Error parsing parameters JSON: {e}")
        return 1

    # Parse allowed categories if provided
    allowed_categories = None
    if args.categories:
        allowed_categories = [c.strip() for c in args.categories.split(',')]

    # Validate parameters
    validator = SearchParamValidator(allowed_categories)
    is_valid, cleaned_params, errors = validator.validate(params)

    # Output results
    result = {
        'valid': is_valid,
        'cleaned_params': cleaned_params,
        'errors': errors
    }

    print(json.dumps(result, indent=2, default=str))

    # Exit code based on validation result
    if args.strict and not is_valid:
        return 1

    return 0


if __name__ == '__main__':
    exit(main())