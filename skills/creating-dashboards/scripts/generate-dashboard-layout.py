#!/usr/bin/env python3
"""
Dashboard Layout Generator
Generates responsive grid layouts based on widget configuration and screen size.
"""

import json
import argparse
from typing import Dict, List, Any, Tuple
import math


class DashboardLayoutGenerator:
    """Generates optimized dashboard layouts for different screen sizes."""

    def __init__(self):
        self.breakpoints = {
            'xxs': {'width': 0, 'cols': 2},
            'xs': {'width': 480, 'cols': 4},
            'sm': {'width': 768, 'cols': 6},
            'md': {'width': 996, 'cols': 10},
            'lg': {'width': 1200, 'cols': 12},
            'xl': {'width': 1920, 'cols': 16}
        }

        self.widget_sizes = {
            'kpi': {'min_w': 2, 'min_h': 2, 'ideal_w': 3, 'ideal_h': 2},
            'chart': {'min_w': 4, 'min_h': 3, 'ideal_w': 6, 'ideal_h': 4},
            'table': {'min_w': 4, 'min_h': 3, 'ideal_w': 6, 'ideal_h': 4},
            'map': {'min_w': 4, 'min_h': 3, 'ideal_w': 8, 'ideal_h': 5},
            'timeline': {'min_w': 6, 'min_h': 2, 'ideal_w': 12, 'ideal_h': 3},
            'text': {'min_w': 2, 'min_h': 1, 'ideal_w': 4, 'ideal_h': 2},
            'gauge': {'min_w': 2, 'min_h': 2, 'ideal_w': 3, 'ideal_h': 3}
        }

    def generate_layout(self, widgets: List[Dict], breakpoint: str = 'lg') -> List[Dict]:
        """
        Generate a layout for the given widgets and breakpoint.

        Args:
            widgets: List of widget configurations
            breakpoint: Screen size breakpoint

        Returns:
            List of positioned widgets with x, y, w, h coordinates
        """
        cols = self.breakpoints[breakpoint]['cols']
        layout = []
        grid = [[False] * cols for _ in range(100)]  # Grid to track occupied cells

        # Sort widgets by priority and size (larger first)
        sorted_widgets = sorted(
            widgets,
            key=lambda w: (
                -w.get('priority', 0),
                -self.widget_sizes.get(w['type'], {}).get('ideal_w', 3) *
                self.widget_sizes.get(w['type'], {}).get('ideal_h', 2)
            )
        )

        for widget in sorted_widgets:
            position = self._find_position(widget, grid, cols, breakpoint)
            if position:
                layout.append({
                    'i': widget['id'],
                    'x': position[0],
                    'y': position[1],
                    'w': position[2],
                    'h': position[3],
                    'minW': self.widget_sizes.get(widget['type'], {}).get('min_w', 2),
                    'minH': self.widget_sizes.get(widget['type'], {}).get('min_h', 2)
                })
                self._mark_occupied(grid, position)

        return layout

    def _find_position(self, widget: Dict, grid: List[List[bool]], cols: int, breakpoint: str) -> Tuple[int, int, int, int]:
        """Find the best position for a widget in the grid."""
        widget_type = widget.get('type', 'kpi')
        size_config = self.widget_sizes.get(widget_type, self.widget_sizes['kpi'])

        # Adjust size based on breakpoint
        if breakpoint in ['xxs', 'xs']:
            # Mobile: full width
            width = cols
            height = size_config['min_h']
        elif breakpoint in ['sm', 'md']:
            # Tablet: half to full width
            width = min(cols, max(cols // 2, size_config['min_w']))
            height = size_config['ideal_h']
        else:
            # Desktop: ideal size
            width = min(cols, size_config['ideal_w'])
            height = size_config['ideal_h']

        # Find first available position
        for y in range(100):
            for x in range(cols - width + 1):
                if self._can_place(grid, x, y, width, height):
                    return (x, y, width, height)

        return None

    def _can_place(self, grid: List[List[bool]], x: int, y: int, w: int, h: int) -> bool:
        """Check if a widget can be placed at the given position."""
        for row in range(y, y + h):
            for col in range(x, x + w):
                if row >= len(grid) or col >= len(grid[0]) or grid[row][col]:
                    return False
        return True

    def _mark_occupied(self, grid: List[List[bool]], position: Tuple[int, int, int, int]):
        """Mark grid cells as occupied."""
        x, y, w, h = position
        for row in range(y, y + h):
            for col in range(x, x + w):
                if row < len(grid) and col < len(grid[0]):
                    grid[row][col] = True

    def generate_responsive_layouts(self, widgets: List[Dict]) -> Dict[str, List[Dict]]:
        """Generate layouts for all breakpoints."""
        layouts = {}
        for breakpoint in self.breakpoints.keys():
            layouts[breakpoint] = self.generate_layout(widgets, breakpoint)
        return layouts

    def optimize_layout(self, layout: List[Dict]) -> List[Dict]:
        """Optimize layout by removing gaps and compacting widgets."""
        # Sort by y position, then x position
        sorted_layout = sorted(layout, key=lambda w: (w['y'], w['x']))

        # Compact vertically
        for i, widget in enumerate(sorted_layout):
            # Try to move widget up
            target_y = 0
            for y in range(widget['y']):
                can_move = True
                for other in sorted_layout[:i]:
                    if (other['x'] < widget['x'] + widget['w'] and
                        widget['x'] < other['x'] + other['w'] and
                        other['y'] <= y < other['y'] + other['h']):
                        can_move = False
                        target_y = other['y'] + other['h']
                        break

                if can_move and y >= target_y:
                    widget['y'] = y
                    break

        return sorted_layout

    def calculate_layout_score(self, layout: List[Dict], widgets: List[Dict]) -> float:
        """Calculate a quality score for the layout."""
        if not layout:
            return 0.0

        score = 100.0

        # Penalize for widgets not placed
        placement_rate = len(layout) / len(widgets) if widgets else 1.0
        score *= placement_rate

        # Penalize for excessive vertical space
        max_y = max(w['y'] + w['h'] for w in layout) if layout else 0
        if max_y > 20:  # Penalize layouts taller than 20 units
            score *= (20 / max_y)

        # Reward for widgets maintaining ideal sizes
        for widget in layout:
            widget_type = next((w['type'] for w in widgets if w['id'] == widget['i']), 'kpi')
            ideal_size = self.widget_sizes.get(widget_type, {})

            if ideal_size:
                size_match = (
                    (widget['w'] / ideal_size.get('ideal_w', widget['w'])) *
                    (widget['h'] / ideal_size.get('ideal_h', widget['h']))
                )
                score += min(10, size_match * 10)

        return round(score, 2)


def create_sample_widgets(count: int = 10) -> List[Dict]:
    """Create sample widget configurations for testing."""
    import random

    widget_types = ['kpi', 'chart', 'table', 'map', 'timeline', 'text', 'gauge']
    widgets = []

    for i in range(count):
        widget_type = random.choice(widget_types)
        widgets.append({
            'id': f'widget-{i+1}',
            'type': widget_type,
            'title': f'{widget_type.capitalize()} Widget {i+1}',
            'priority': random.randint(1, 5)
        })

    return widgets


def export_to_react(layouts: Dict[str, List[Dict]]) -> str:
    """Export layouts as React component code."""
    code = """// Generated Dashboard Layouts
export const dashboardLayouts = {
"""

    for breakpoint, layout in layouts.items():
        code += f"  {breakpoint}: [\n"
        for widget in layout:
            code += f"    {json.dumps(widget)},\n"
        code += "  ],\n"

    code += "};\n"
    return code


def main():
    """Main function to run the layout generator."""
    parser = argparse.ArgumentParser(description='Generate dashboard layouts')
    parser.add_argument('--config', type=str, help='Path to widget configuration JSON file')
    parser.add_argument('--widgets', type=int, default=10, help='Number of sample widgets to generate')
    parser.add_argument('--breakpoint', type=str, default='all', help='Specific breakpoint or "all"')
    parser.add_argument('--optimize', action='store_true', help='Optimize the layout')
    parser.add_argument('--export', type=str, choices=['json', 'react'], default='json', help='Export format')
    parser.add_argument('--output', type=str, help='Output file path')

    args = parser.parse_args()

    generator = DashboardLayoutGenerator()

    # Load or create widgets
    if args.config:
        with open(args.config, 'r') as f:
            widgets = json.load(f)
    else:
        widgets = create_sample_widgets(args.widgets)
        print(f"Generated {len(widgets)} sample widgets")

    # Generate layouts
    if args.breakpoint == 'all':
        layouts = generator.generate_responsive_layouts(widgets)
    else:
        layout = generator.generate_layout(widgets, args.breakpoint)
        if args.optimize:
            layout = generator.optimize_layout(layout)
        layouts = {args.breakpoint: layout}

    # Calculate scores
    print("\nLayout Quality Scores:")
    for breakpoint, layout in layouts.items():
        score = generator.calculate_layout_score(layout, widgets)
        print(f"  {breakpoint}: {score}/100")

    # Export results
    if args.export == 'react':
        output = export_to_react(layouts)
    else:
        output = json.dumps(layouts, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nLayout saved to {args.output}")
    else:
        print("\nGenerated Layout:")
        print(output)


if __name__ == '__main__':
    main()