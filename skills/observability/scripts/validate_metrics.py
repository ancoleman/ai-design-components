#!/usr/bin/env python3
"""
Validate OpenTelemetry Metric Naming and Configuration

Checks metric names, labels, and configuration against OpenTelemetry semantic conventions.

Usage:
    python scripts/validate_metrics.py --metrics metrics.json
    python scripts/validate_metrics.py --endpoint http://localhost:9090/api/v1/label/__name__/values
"""

import argparse
import json
import re
import sys
from typing import List, Dict, Set
import requests


# OpenTelemetry metric naming conventions
VALID_METRIC_PATTERNS = {
    # HTTP metrics
    r'^http\.server\.(request|duration|active_requests)$',
    r'^http\.client\.(request|duration)$',

    # Database metrics
    r'^db\.client\.(connections|operations)$',

    # System metrics
    r'^system\.(cpu|memory|disk|network)\.\w+$',

    # Custom metrics (must follow pattern)
    r'^[a-z][a-z0-9_]*\.(count|gauge|histogram|summary)$',
}

REQUIRED_LABELS = {
    "http.server.request": ["method", "status"],
    "http.server.duration": ["method", "route"],
    "db.client.connections": ["state", "pool_name"],
}

RESERVED_LABELS = {"le", "quantile"}  # Prometheus reserved


def validate_metric_name(name: str) -> List[str]:
    """Validate metric name follows conventions"""
    errors = []

    # Must be lowercase with underscores or dots
    if not re.match(r'^[a-z][a-z0-9_.]*$', name):
        errors.append(f"Invalid characters in '{name}' (use lowercase, digits, underscores, dots)")

    # Must not end with underscore/dot
    if name.endswith('_') or name.endswith('.'):
        errors.append(f"Metric '{name}' cannot end with underscore or dot")

    # Check against patterns
    valid = any(re.match(pattern, name) for pattern in VALID_METRIC_PATTERNS)
    if not valid:
        errors.append(f"Metric '{name}' doesn't match OTel semantic conventions")

    return errors


def validate_labels(metric: str, labels: Set[str]) -> List[str]:
    """Validate metric labels"""
    errors = []

    # Check for reserved labels
    reserved_used = labels.intersection(RESERVED_LABELS)
    if reserved_used:
        errors.append(f"Metric '{metric}' uses reserved labels: {reserved_used}")

    # Check required labels
    if metric in REQUIRED_LABELS:
        required = set(REQUIRED_LABELS[metric])
        missing = required - labels

        if missing:
            errors.append(f"Metric '{metric}' missing required labels: {missing}")

    # Label names must be lowercase with underscores
    for label in labels:
        if not re.match(r'^[a-z][a-z0-9_]*$', label):
            errors.append(f"Invalid label '{label}' in '{metric}' (use lowercase and underscores)")

    return errors


def fetch_metrics_from_prometheus(endpoint: str) -> List[str]:
    """Fetch metric names from Prometheus"""
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching from Prometheus: {e}", file=sys.stderr)
        sys.exit(1)


def load_metrics_from_file(file_path: str) -> Dict[str, Set[str]]:
    """Load metrics from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Expected format: {"metric_name": ["label1", "label2"]}
    return {k: set(v) for k, v in data.items()}


def main():
    parser = argparse.ArgumentParser(description="Validate OpenTelemetry metrics")
    parser.add_argument(
        "--metrics",
        help="Path to metrics JSON file"
    )
    parser.add_argument(
        "--endpoint",
        help="Prometheus API endpoint for metric names"
    )

    args = parser.parse_args()

    if not args.metrics and not args.endpoint:
        print("Error: Must provide --metrics or --endpoint", file=sys.stderr)
        sys.exit(1)

    # Load metrics
    if args.metrics:
        print(f"Loading metrics from: {args.metrics}")
        metrics = load_metrics_from_file(args.metrics)
    else:
        print(f"Fetching metrics from: {args.endpoint}")
        metric_names = fetch_metrics_from_prometheus(args.endpoint)
        metrics = {name: set() for name in metric_names}  # No labels from Prometheus API

    print(f"Validating {len(metrics)} metrics...")
    print("-" * 60)

    all_errors = []
    valid_count = 0

    for metric_name, labels in sorted(metrics.items()):
        errors = []

        # Validate name
        name_errors = validate_metric_name(metric_name)
        errors.extend(name_errors)

        # Validate labels (if provided)
        if labels:
            label_errors = validate_labels(metric_name, labels)
            errors.extend(label_errors)

        if errors:
            print(f"\n✗ {metric_name}")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend(errors)
        else:
            print(f"✓ {metric_name}")
            valid_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Validation Summary:")
    print(f"  Total metrics: {len(metrics)}")
    print(f"  Valid: {valid_count}")
    print(f"  Invalid: {len(metrics) - valid_count}")
    print(f"  Total errors: {len(all_errors)}")

    if all_errors:
        print("\n⚠ Validation failed. Fix errors above.")
        sys.exit(1)
    else:
        print("\n✓ All metrics valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
