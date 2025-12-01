#!/usr/bin/env python3

"""
Message Formatting Utilities for User Feedback

Formats user-facing messages based on error codes, operation types,
and context. Provides consistent, friendly messaging across the application.

Usage: python format_messages.py [options]

Options:
  --type <type>        Message type (error, success, warning, info)
  --code <code>        Error/status code
  --context <context>  Operation context (upload, save, delete, etc.)
  --data <json>        Additional data as JSON
"""

import sys
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime

# Error code mappings
ERROR_MESSAGES = {
    # Network errors
    'NETWORK_ERROR': 'Connection lost. Please check your internet connection.',
    'TIMEOUT': 'The operation took too long. Please try again.',
    'SERVER_ERROR': 'Something went wrong on our end. Please try again later.',
    'SERVICE_UNAVAILABLE': 'Service temporarily unavailable. Please try again in a few moments.',

    # Auth errors
    'UNAUTHORIZED': 'You need to sign in to continue.',
    'FORBIDDEN': 'You don\'t have permission to perform this action.',
    'SESSION_EXPIRED': 'Your session has expired. Please sign in again.',
    'INVALID_CREDENTIALS': 'Invalid email or password.',

    # Validation errors
    'VALIDATION_ERROR': 'Please check the form and fix any errors.',
    'REQUIRED_FIELD': '{field} is required.',
    'INVALID_FORMAT': '{field} format is invalid.',
    'VALUE_TOO_LONG': '{field} is too long (maximum {max} characters).',
    'VALUE_TOO_SHORT': '{field} is too short (minimum {min} characters).',

    # File errors
    'FILE_TOO_LARGE': 'File is too large. Maximum size is {max_size}.',
    'INVALID_FILE_TYPE': 'Invalid file type. Allowed types: {allowed_types}.',
    'UPLOAD_FAILED': 'Failed to upload {filename}. Please try again.',
    'FILE_NOT_FOUND': 'File not found.',

    # Data errors
    'NOT_FOUND': 'The requested item could not be found.',
    'ALREADY_EXISTS': 'An item with this name already exists.',
    'CONFLICT': 'This action conflicts with recent changes.',
    'STALE_DATA': 'This data has been modified. Please refresh and try again.',

    # Rate limiting
    'RATE_LIMITED': 'Too many requests. Please wait {retry_after} seconds.',
    'QUOTA_EXCEEDED': 'You\'ve reached your usage limit. Please upgrade your plan.',

    # Generic
    'UNKNOWN_ERROR': 'An unexpected error occurred. Please try again.',
}

# Success message templates
SUCCESS_MESSAGES = {
    'save': '{item} saved successfully.',
    'create': '{item} created successfully.',
    'update': '{item} updated successfully.',
    'delete': '{item} deleted successfully.',
    'upload': '{filename} uploaded successfully.',
    'download': 'Download started.',
    'copy': '{item} copied to clipboard.',
    'share': '{item} shared successfully.',
    'send': 'Message sent successfully.',
    'submit': 'Form submitted successfully.',
    'publish': '{item} published successfully.',
    'archive': '{item} archived successfully.',
    'restore': '{item} restored successfully.',
    'export': 'Export completed successfully.',
    'import': 'Import completed successfully.',
    'sync': 'Sync completed successfully.',
}

# Warning message templates
WARNING_MESSAGES = {
    'unsaved_changes': 'You have unsaved changes. Are you sure you want to leave?',
    'delete_confirmation': 'Are you sure you want to delete {item}? This cannot be undone.',
    'bulk_action': 'This will affect {count} items. Do you want to continue?',
    'storage_warning': 'You\'re using {percentage}% of your storage.',
    'expiring_soon': 'Your {item} expires in {days} days.',
    'deprecated_feature': 'This feature will be removed in the next version.',
    'slow_connection': 'Slow connection detected. Some features may be limited.',
    'partial_success': 'Operation partially completed. {succeeded} succeeded, {failed} failed.',
}

# Info message templates
INFO_MESSAGES = {
    'loading': 'Loading {item}...',
    'processing': 'Processing your request...',
    'saving': 'Saving {item}...',
    'uploading': 'Uploading {filename}... {progress}%',
    'downloading': 'Downloading {filename}... {progress}%',
    'searching': 'Searching for {query}...',
    'no_results': 'No results found for "{query}".',
    'empty_state': 'No {items} yet. Create your first one to get started.',
    'tip': 'Tip: {message}',
    'update_available': 'A new version is available. Click to update.',
}


def format_message(
    message_type: str,
    code: Optional[str] = None,
    context: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a message based on type, code, and context.

    Args:
        message_type: Type of message (error, success, warning, info)
        code: Error/status code
        context: Operation context
        data: Additional data for message formatting

    Returns:
        Formatted message with metadata
    """
    data = data or {}

    if message_type == 'error':
        message = format_error_message(code, data)
        severity = 'high' if code in ['SERVER_ERROR', 'UNAUTHORIZED'] else 'medium'
    elif message_type == 'success':
        message = format_success_message(context, data)
        severity = 'low'
    elif message_type == 'warning':
        message = format_warning_message(context, data)
        severity = 'medium'
    elif message_type == 'info':
        message = format_info_message(context, data)
        severity = 'low'
    else:
        message = 'Unknown message type'
        severity = 'low'

    return {
        'type': message_type,
        'message': message,
        'severity': severity,
        'timestamp': datetime.now().isoformat(),
        'code': code,
        'context': context,
        'data': data,
        'suggestions': get_suggestions(message_type, code),
        'actions': get_actions(message_type, code, context)
    }


def format_error_message(code: Optional[str], data: Dict[str, Any]) -> str:
    """Format error message based on error code."""
    if not code:
        return ERROR_MESSAGES['UNKNOWN_ERROR']

    template = ERROR_MESSAGES.get(code, ERROR_MESSAGES['UNKNOWN_ERROR'])

    try:
        return template.format(**data)
    except KeyError:
        return template


def format_success_message(context: Optional[str], data: Dict[str, Any]) -> str:
    """Format success message based on context."""
    if not context:
        return 'Operation completed successfully.'

    template = SUCCESS_MESSAGES.get(context, 'Operation completed successfully.')

    # Set default item name if not provided
    if '{item}' in template and 'item' not in data:
        data['item'] = context.replace('_', ' ').title()

    try:
        return template.format(**data)
    except KeyError:
        return template


def format_warning_message(context: Optional[str], data: Dict[str, Any]) -> str:
    """Format warning message based on context."""
    if not context:
        return 'Please proceed with caution.'

    template = WARNING_MESSAGES.get(context, 'Please proceed with caution.')

    try:
        return template.format(**data)
    except KeyError:
        return template


def format_info_message(context: Optional[str], data: Dict[str, Any]) -> str:
    """Format info message based on context."""
    if not context:
        return 'Processing...'

    template = INFO_MESSAGES.get(context, 'Processing...')

    try:
        return template.format(**data)
    except KeyError:
        return template


def get_suggestions(message_type: str, code: Optional[str]) -> List[str]:
    """Get suggestions based on message type and code."""
    suggestions = []

    if message_type == 'error':
        if code == 'NETWORK_ERROR':
            suggestions = [
                'Check your internet connection',
                'Try refreshing the page',
                'Check if you\'re behind a firewall'
            ]
        elif code == 'VALIDATION_ERROR':
            suggestions = [
                'Review the highlighted fields',
                'Check for required fields',
                'Ensure formats are correct'
            ]
        elif code == 'UNAUTHORIZED':
            suggestions = [
                'Sign in to your account',
                'Check your credentials',
                'Request a password reset if needed'
            ]
        elif code == 'FILE_TOO_LARGE':
            suggestions = [
                'Compress the file',
                'Split into smaller files',
                'Upgrade your plan for larger uploads'
            ]

    return suggestions


def get_actions(message_type: str, code: Optional[str], context: Optional[str]) -> List[Dict[str, str]]:
    """Get available actions based on message type, code, and context."""
    actions = []

    if message_type == 'error':
        actions.append({'label': 'Try Again', 'action': 'retry'})

        if code == 'UNAUTHORIZED':
            actions.append({'label': 'Sign In', 'action': 'signin'})
        elif code == 'NETWORK_ERROR':
            actions.append({'label': 'Refresh', 'action': 'refresh'})
        elif code == 'QUOTA_EXCEEDED':
            actions.append({'label': 'Upgrade Plan', 'action': 'upgrade'})

    elif message_type == 'success':
        if context in ['create', 'save', 'update']:
            actions.append({'label': 'View', 'action': 'view'})
            actions.append({'label': 'Create Another', 'action': 'create_new'})
        elif context == 'delete':
            actions.append({'label': 'Undo', 'action': 'undo'})

    elif message_type == 'warning':
        if context == 'delete_confirmation':
            actions.append({'label': 'Cancel', 'action': 'cancel', 'primary': False})
            actions.append({'label': 'Delete', 'action': 'confirm', 'primary': True, 'destructive': True})
        elif context == 'unsaved_changes':
            actions.append({'label': 'Stay', 'action': 'stay', 'primary': False})
            actions.append({'label': 'Leave', 'action': 'leave', 'primary': True})

    return actions


def humanize_error_code(code: str) -> str:
    """Convert error code to human-readable format."""
    return code.replace('_', ' ').title()


def format_file_size(bytes_size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f'{bytes_size:.1f} {unit}'
        bytes_size /= 1024
    return f'{bytes_size:.1f} TB'


def format_time_remaining(seconds: int) -> str:
    """Format time remaining in human-readable format."""
    if seconds < 60:
        return f'{seconds} seconds'
    elif seconds < 3600:
        return f'{seconds // 60} minutes'
    elif seconds < 86400:
        return f'{seconds // 3600} hours'
    else:
        return f'{seconds // 86400} days'


def parse_http_error(status_code: int, response_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Parse HTTP error and return formatted message."""
    error_map = {
        400: 'VALIDATION_ERROR',
        401: 'UNAUTHORIZED',
        403: 'FORBIDDEN',
        404: 'NOT_FOUND',
        409: 'CONFLICT',
        429: 'RATE_LIMITED',
        500: 'SERVER_ERROR',
        503: 'SERVICE_UNAVAILABLE'
    }

    code = error_map.get(status_code, 'UNKNOWN_ERROR')

    # Extract additional data from response
    data = {}
    if response_data:
        data = {
            'field': response_data.get('field'),
            'details': response_data.get('details'),
            'retry_after': response_data.get('retry_after')
        }

    return format_message('error', code, None, data)


def main():
    """Main function for CLI usage."""
    # Parse command line arguments
    args = {}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1

    # Parse data if provided
    data = {}
    if 'data' in args:
        try:
            data = json.loads(args['data'])
        except json.JSONDecodeError:
            print('Error: Invalid JSON data')
            return

    # Format message
    result = format_message(
        message_type=args.get('type', 'info'),
        code=args.get('code'),
        context=args.get('context'),
        data=data
    )

    # Output result
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()