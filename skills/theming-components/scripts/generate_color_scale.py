#!/usr/bin/env python3
"""
Generate a 9-shade color scale from a base color.

Usage:
    python generate_color_scale.py --base "#3B82F6" --name "blue"

Outputs W3C format JSON for use in tokens/global/colors.json
"""

import argparse
import json
import colorsys


def hex_to_hsl(hex_color):
    """Convert hex color to HSL."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def hsl_to_hex(h, s, l):
    """Convert HSL to hex color."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#{:02X}{:02X}{:02X}'.format(
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )


def generate_scale(base_hex, name):
    """
    Generate 9-shade color scale.

    Shades:
    - 50: Lightest (backgrounds)
    - 100-400: Light shades
    - 500: Base color (provided)
    - 600-900: Dark shades
    """
    h, s, l = hex_to_hsl(base_hex)

    # Lightness adjustments for each shade
    # 50 is lightest, 500 is base, 900 is darkest
    lightness_map = {
        50: 0.96,
        100: 0.92,
        200: 0.84,
        300: 0.72,
        400: 0.60,
        500: l,  # Base lightness
        600: l - 0.10,
        700: l - 0.20,
        800: l - 0.28,
        900: l - 0.35
    }

    scale = {}
    for shade, target_lightness in lightness_map.items():
        # Clamp lightness between 0 and 1
        clamped_lightness = max(0, min(1, target_lightness))
        hex_color = hsl_to_hex(h, s, clamped_lightness)

        scale[str(shade)] = {
            "$value": hex_color,
            "$type": "color"
        }

        # Add description for key shades
        if shade == 50:
            scale[str(shade)]["$description"] = f"Lightest {name} - backgrounds"
        elif shade == 500:
            scale[str(shade)]["$description"] = f"Base {name}"
        elif shade == 900:
            scale[str(shade)]["$description"] = f"Darkest {name}"

    return scale


def main():
    parser = argparse.ArgumentParser(
        description='Generate a 9-shade color scale from a base color'
    )
    parser.add_argument(
        '--base',
        required=True,
        help='Base color in hex format (e.g., #3B82F6)'
    )
    parser.add_argument(
        '--name',
        required=True,
        help='Color name (e.g., blue, red, brand-primary)'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file path (optional, defaults to stdout)'
    )

    args = parser.parse_args()

    # Generate scale
    scale = generate_scale(args.base, args.name)

    # Wrap in W3C format
    output = {
        "$schema": "https://design-tokens.org/community-group/format/1.0.0",
        "color": {
            args.name: scale
        }
    }

    # Output
    json_str = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_str)
        print(f"✅ Color scale '{args.name}' generated at {args.output}")
    else:
        print(json_str)


if __name__ == '__main__':
    main()
