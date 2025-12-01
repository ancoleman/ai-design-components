#!/usr/bin/env python3
"""
Widget Configuration Validator
Validates widget configurations, data bindings, and filter relationships.
"""

import json
import argparse
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of a validation check."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_info(self, message: str):
        self.info.append(message)

    def merge(self, other: 'ValidationResult'):
        self.is_valid = self.is_valid and other.is_valid
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)


class WidgetConfigValidator:
    """Validates dashboard widget configurations."""

    def __init__(self):
        self.valid_widget_types = {
            'kpi', 'chart', 'table', 'map', 'timeline',
            'gauge', 'text', 'filter', 'image', 'custom'
        }

        self.required_fields = {
            'all': ['id', 'type'],
            'kpi': ['metric', 'data_source'],
            'chart': ['chart_type', 'data_source', 'axes'],
            'table': ['columns', 'data_source'],
            'filter': ['filter_type', 'options']
        }

        self.valid_chart_types = {
            'line', 'bar', 'area', 'pie', 'donut', 'scatter',
            'bubble', 'radar', 'treemap', 'heatmap', 'sankey'
        }

        self.valid_filter_types = {
            'select', 'multiselect', 'date_range', 'search',
            'checkbox', 'radio', 'slider', 'toggle'
        }

        self.valid_aggregations = {
            'sum', 'average', 'median', 'min', 'max',
            'count', 'distinct', 'percentile', 'std_dev'
        }

    def validate_widget(self, widget: Dict) -> ValidationResult:
        """Validate a single widget configuration."""
        result = ValidationResult(is_valid=True)

        # Check required fields
        for field in self.required_fields['all']:
            if field not in widget:
                result.add_error(f"Widget missing required field: {field}")

        if not result.is_valid:
            return result

        widget_id = widget.get('id')
        widget_type = widget.get('type')

        # Validate widget type
        if widget_type not in self.valid_widget_types:
            result.add_error(f"Widget {widget_id}: Invalid type '{widget_type}'")
            return result

        # Type-specific validation
        type_validator = getattr(self, f'_validate_{widget_type}_widget', None)
        if type_validator:
            type_result = type_validator(widget)
            result.merge(type_result)

        # Validate common properties
        self._validate_common_properties(widget, result)

        return result

    def _validate_kpi_widget(self, widget: Dict) -> ValidationResult:
        """Validate KPI widget configuration."""
        result = ValidationResult(is_valid=True)

        # Check required KPI fields
        for field in self.required_fields['kpi']:
            if field not in widget:
                result.add_error(f"KPI widget {widget['id']}: Missing field '{field}'")

        # Validate aggregation
        aggregation = widget.get('aggregation')
        if aggregation and aggregation not in self.valid_aggregations:
            result.add_error(f"KPI widget {widget['id']}: Invalid aggregation '{aggregation}'")

        # Validate format
        format_type = widget.get('format')
        valid_formats = {'number', 'currency', 'percentage', 'decimal', 'compact'}
        if format_type and format_type not in valid_formats:
            result.add_warning(f"KPI widget {widget['id']}: Unknown format '{format_type}'")

        # Check trend configuration
        if 'trend' in widget:
            trend = widget['trend']
            if not isinstance(trend, dict):
                result.add_error(f"KPI widget {widget['id']}: Trend must be an object")
            elif 'comparison' not in trend:
                result.add_warning(f"KPI widget {widget['id']}: Trend missing comparison period")

        return result

    def _validate_chart_widget(self, widget: Dict) -> ValidationResult:
        """Validate chart widget configuration."""
        result = ValidationResult(is_valid=True)

        # Check required chart fields
        for field in self.required_fields['chart']:
            if field not in widget:
                result.add_error(f"Chart widget {widget['id']}: Missing field '{field}'")

        # Validate chart type
        chart_type = widget.get('chart_type')
        if chart_type and chart_type not in self.valid_chart_types:
            result.add_error(f"Chart widget {widget['id']}: Invalid chart type '{chart_type}'")

        # Validate axes configuration
        axes = widget.get('axes')
        if axes:
            if not isinstance(axes, dict):
                result.add_error(f"Chart widget {widget['id']}: Axes must be an object")
            else:
                if chart_type in ['line', 'bar', 'area', 'scatter'] and 'x' not in axes:
                    result.add_error(f"Chart widget {widget['id']}: Missing x-axis configuration")

        return result

    def _validate_table_widget(self, widget: Dict) -> ValidationResult:
        """Validate table widget configuration."""
        result = ValidationResult(is_valid=True)

        # Check required table fields
        for field in self.required_fields['table']:
            if field not in widget:
                result.add_error(f"Table widget {widget['id']}: Missing field '{field}'")

        # Validate columns
        columns = widget.get('columns')
        if columns:
            if not isinstance(columns, list):
                result.add_error(f"Table widget {widget['id']}: Columns must be an array")
            elif not columns:
                result.add_error(f"Table widget {widget['id']}: Columns array is empty")
            else:
                for i, col in enumerate(columns):
                    if not isinstance(col, dict):
                        result.add_error(f"Table widget {widget['id']}: Column {i} must be an object")
                    elif 'field' not in col:
                        result.add_error(f"Table widget {widget['id']}: Column {i} missing 'field'")

        # Check pagination settings
        if 'pagination' in widget:
            pagination = widget['pagination']
            if isinstance(pagination, dict):
                if 'pageSize' in pagination and not isinstance(pagination['pageSize'], int):
                    result.add_warning(f"Table widget {widget['id']}: pageSize should be an integer")

        return result

    def _validate_filter_widget(self, widget: Dict) -> ValidationResult:
        """Validate filter widget configuration."""
        result = ValidationResult(is_valid=True)

        # Check required filter fields
        for field in self.required_fields['filter']:
            if field not in widget:
                result.add_error(f"Filter widget {widget['id']}: Missing field '{field}'")

        # Validate filter type
        filter_type = widget.get('filter_type')
        if filter_type and filter_type not in self.valid_filter_types:
            result.add_error(f"Filter widget {widget['id']}: Invalid filter type '{filter_type}'")

        # Validate options
        options = widget.get('options')
        if filter_type in ['select', 'multiselect', 'radio', 'checkbox']:
            if not options:
                result.add_error(f"Filter widget {widget['id']}: Options required for {filter_type}")
            elif not isinstance(options, list):
                result.add_error(f"Filter widget {widget['id']}: Options must be an array")

        # Validate target widgets
        if 'target_widgets' in widget:
            targets = widget['target_widgets']
            if not isinstance(targets, list):
                result.add_warning(f"Filter widget {widget['id']}: target_widgets should be an array")

        return result

    def _validate_common_properties(self, widget: Dict, result: ValidationResult):
        """Validate common widget properties."""
        widget_id = widget['id']

        # Validate position if present
        if 'position' in widget:
            position = widget['position']
            required_pos_fields = ['x', 'y', 'w', 'h']

            for field in required_pos_fields:
                if field not in position:
                    result.add_warning(f"Widget {widget_id}: Position missing field '{field}'")
                elif not isinstance(position[field], (int, float)):
                    result.add_error(f"Widget {widget_id}: Position field '{field}' must be numeric")

            # Check for reasonable values
            if position.get('w', 0) < 1 or position.get('h', 0) < 1:
                result.add_error(f"Widget {widget_id}: Width and height must be >= 1")

            if position.get('x', 0) < 0 or position.get('y', 0) < 0:
                result.add_error(f"Widget {widget_id}: Position x,y must be >= 0")

        # Validate refresh interval
        if 'refresh_interval' in widget:
            interval = widget['refresh_interval']
            if not isinstance(interval, (int, float)):
                result.add_error(f"Widget {widget_id}: refresh_interval must be numeric")
            elif interval < 0:
                result.add_error(f"Widget {widget_id}: refresh_interval must be >= 0")
            elif interval > 0 and interval < 1000:
                result.add_warning(f"Widget {widget_id}: refresh_interval < 1000ms may impact performance")

        # Validate data source
        if 'data_source' in widget:
            data_source = widget['data_source']
            if not isinstance(data_source, (str, dict)):
                result.add_error(f"Widget {widget_id}: data_source must be string or object")

    def validate_dashboard(self, dashboard: Dict) -> ValidationResult:
        """Validate entire dashboard configuration."""
        result = ValidationResult(is_valid=True)

        # Check dashboard metadata
        if 'widgets' not in dashboard:
            result.add_error("Dashboard missing 'widgets' array")
            return result

        widgets = dashboard['widgets']
        if not isinstance(widgets, list):
            result.add_error("Dashboard 'widgets' must be an array")
            return result

        if not widgets:
            result.add_warning("Dashboard has no widgets")
            return result

        # Validate each widget
        widget_ids = set()
        for i, widget in enumerate(widgets):
            if not isinstance(widget, dict):
                result.add_error(f"Widget at index {i} must be an object")
                continue

            widget_result = self.validate_widget(widget)
            result.merge(widget_result)

            # Check for duplicate IDs
            widget_id = widget.get('id')
            if widget_id:
                if widget_id in widget_ids:
                    result.add_error(f"Duplicate widget ID: {widget_id}")
                widget_ids.add(widget_id)

        # Validate widget relationships
        self._validate_relationships(dashboard, result)

        # Check layout conflicts
        self._check_layout_conflicts(widgets, result)

        return result

    def _validate_relationships(self, dashboard: Dict, result: ValidationResult):
        """Validate relationships between widgets."""
        widgets = dashboard['widgets']
        widget_ids = {w['id'] for w in widgets if 'id' in w}

        # Check filter targets
        for widget in widgets:
            if widget.get('type') == 'filter' and 'target_widgets' in widget:
                for target_id in widget['target_widgets']:
                    if target_id not in widget_ids:
                        result.add_warning(
                            f"Filter {widget['id']}: Target widget '{target_id}' not found"
                        )

        # Check data dependencies
        for widget in widgets:
            if 'depends_on' in widget:
                deps = widget['depends_on']
                if isinstance(deps, list):
                    for dep_id in deps:
                        if dep_id not in widget_ids:
                            result.add_error(
                                f"Widget {widget['id']}: Dependency '{dep_id}' not found"
                            )

    def _check_layout_conflicts(self, widgets: List[Dict], result: ValidationResult):
        """Check for overlapping widget positions."""
        positioned_widgets = [w for w in widgets if 'position' in w]

        for i, widget1 in enumerate(positioned_widgets):
            pos1 = widget1['position']
            for widget2 in positioned_widgets[i+1:]:
                pos2 = widget2['position']

                # Check for overlap
                if self._positions_overlap(pos1, pos2):
                    result.add_warning(
                        f"Widgets {widget1['id']} and {widget2['id']} have overlapping positions"
                    )

    def _positions_overlap(self, pos1: Dict, pos2: Dict) -> bool:
        """Check if two positions overlap."""
        x1, y1, w1, h1 = pos1.get('x', 0), pos1.get('y', 0), pos1.get('w', 1), pos1.get('h', 1)
        x2, y2, w2, h2 = pos2.get('x', 0), pos2.get('y', 0), pos2.get('w', 1), pos2.get('h', 1)

        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)


def main():
    """Main function to run the validator."""
    parser = argparse.ArgumentParser(description='Validate dashboard widget configurations')
    parser.add_argument('--config', type=str, required=True, help='Path to dashboard configuration JSON file')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    parser.add_argument('--output', type=str, help='Output validation report to file')

    args = parser.parse_args()

    validator = WidgetConfigValidator()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            dashboard = json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return 1

    # Validate
    result = validator.validate_dashboard(dashboard)

    # Treat warnings as errors if strict mode
    if args.strict and result.warnings:
        result.is_valid = False

    # Display results
    print("Dashboard Validation Report")
    print("=" * 50)
    print(f"Valid: {'✅ Yes' if result.is_valid else '❌ No'}")

    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  ❌ {error}")

    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  ⚠️  {warning}")

    if result.info:
        print(f"\nInfo ({len(result.info)}):")
        for info in result.info:
            print(f"  ℹ️  {info}")

    if result.is_valid and not result.warnings:
        print("\n✅ Dashboard configuration is valid!")

    # Save report if requested
    if args.output:
        report = {
            'valid': result.is_valid,
            'errors': result.errors,
            'warnings': result.warnings,
            'info': result.info,
            'summary': {
                'error_count': len(result.errors),
                'warning_count': len(result.warnings),
                'info_count': len(result.info)
            }
        }

        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to: {args.output}")

    return 0 if result.is_valid else 1


if __name__ == '__main__':
    exit(main())