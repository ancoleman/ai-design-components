#!/usr/bin/env python3
"""
Message Schema Validator
Validate JSON messages against schemas (JSON Schema, Avro)
"""
import argparse
import json
import sys
from typing import Dict, Any
try:
    from jsonschema import validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("⚠️ jsonschema not installed. Install: pip install jsonschema")


# Example schemas
EVENT_SCHEMAS = {
    "order.created.v1": {
        "type": "object",
        "required": ["event_id", "event_type", "timestamp", "data"],
        "properties": {
            "event_id": {"type": "string", "format": "uuid"},
            "event_type": {"type": "string", "const": "order.created.v1"},
            "timestamp": {"type": "string", "format": "date-time"},
            "version": {"type": "string"},
            "data": {
                "type": "object",
                "required": ["order_id", "customer_id", "total"],
                "properties": {
                    "order_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["item_id", "quantity", "price"],
                            "properties": {
                                "item_id": {"type": "string"},
                                "quantity": {"type": "integer", "minimum": 1},
                                "price": {"type": "number", "minimum": 0}
                            }
                        }
                    },
                    "total": {"type": "number", "minimum": 0}
                }
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "correlation_id": {"type": "string"},
                    "trace_id": {"type": "string"},
                    "user_id": {"type": "string"}
                }
            }
        }
    },
    "payment.charged.v1": {
        "type": "object",
        "required": ["event_id", "event_type", "timestamp", "data"],
        "properties": {
            "event_id": {"type": "string"},
            "event_type": {"type": "string", "const": "payment.charged.v1"},
            "timestamp": {"type": "string"},
            "data": {
                "type": "object",
                "required": ["payment_id", "order_id", "amount", "currency"],
                "properties": {
                    "payment_id": {"type": "string"},
                    "order_id": {"type": "string"},
                    "amount": {"type": "number", "minimum": 0},
                    "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
                    "payment_method": {"type": "string"}
                }
            }
        }
    }
}


def validate_message(message: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate message against JSON schema

    Args:
        message: Message to validate
        schema: JSON schema

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    if not JSONSCHEMA_AVAILABLE:
        print("❌ jsonschema library not available")
        return False

    validate(instance=message, schema=schema)
    return True


def validate_event_message(message: Dict[str, Any]) -> bool:
    """
    Validate event message format

    Args:
        message: Event message

    Returns:
        True if valid
    """
    # Get event type
    event_type = message.get('event_type')

    if not event_type:
        print("❌ Missing event_type field")
        return False

    # Find schema for event type
    schema = EVENT_SCHEMAS.get(event_type)

    if not schema:
        print(f"⚠️ No schema found for event type: {event_type}")
        print(f"Available schemas: {list(EVENT_SCHEMAS.keys())}")
        return False

    # Validate against schema
    try:
        validate_message(message, schema)
        print(f"✅ Message valid for schema: {event_type}")
        return True
    except ValidationError as e:
        print(f"❌ Validation failed: {e.message}")
        print(f"Path: {' -> '.join(str(p) for p in e.path)}")
        return False


def load_schema_file(schema_path: str) -> Dict[str, Any]:
    """Load JSON schema from file"""
    with open(schema_path, 'r') as f:
        return json.load(f)


def load_message_file(message_path: str) -> Dict[str, Any]:
    """Load message from file"""
    with open(message_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Validate message schemas')
    parser.add_argument('message', help='Message JSON file or string')
    parser.add_argument('--schema', help='Schema JSON file (optional)')
    parser.add_argument('--stdin', action='store_true', help='Read message from stdin')

    args = parser.parse_args()

    # Load message
    if args.stdin:
        message_str = sys.stdin.read()
        message = json.loads(message_str)
    elif args.message.endswith('.json'):
        message = load_message_file(args.message)
    else:
        message = json.loads(args.message)

    # Load schema if provided
    if args.schema:
        schema = load_schema_file(args.schema)
        try:
            validate_message(message, schema)
            print("✅ Message is valid")
            return 0
        except ValidationError as e:
            print(f"❌ Validation failed: {e.message}")
            return 1
    else:
        # Validate as event message
        valid = validate_event_message(message)
        return 0 if valid else 1


if __name__ == '__main__':
    sys.exit(main())
