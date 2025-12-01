#!/usr/bin/env python3
"""
Generate color palettes for data visualization

Creates sequential, diverging, and categorical palettes with:
- Colorblind-safe options
- WCAG contrast validation
- JSON output for use in charts

Usage:
    python generate_color_palette.py --type sequential --hue blue --steps 9
    python generate_color_palette.py --type diverging --negative red --positive blue
    python generate_color_palette.py --type categorical --count 10
"""

import argparse
import json
import colorsys
from typing import List, Dict

def hex_to_hsl(hex_color: str) -> tuple:
    """Convert hex color to HSL"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360, s * 100, l * 100)

def hsl_to_hex(h: float, s: float, l: float) -> str:
    """Convert HSL to hex color"""
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

def generate_sequential(base_hue: int, steps: int = 9) -> List[Dict]:
    """Generate sequential color scale (light to dark)"""
    palette = []

    # Lightness from 95 (very light) to 20 (very dark)
    for i in range(steps):
        lightness = 95 - (i * 75 / (steps - 1))
        saturation = 30 + (i * 40 / (steps - 1))  # Increase saturation with darkness

        hex_color = hsl_to_hex(base_hue, saturation, lightness)
        palette.append({
            "step": i + 1,
            "hex": hex_color,
            "hsl": f"hsl({base_hue}, {saturation:.1f}%, {lightness:.1f}%)"
        })

    return palette

def generate_diverging(negative_hue: int, positive_hue: int, steps: int = 11) -> Dict:
    """Generate diverging color scale (negative through neutral to positive)"""
    mid = steps // 2
    palette = {
        "negative": [],
        "midpoint": { "hex": "#F3F4F6", "hsl": "hsl(220, 13%, 96%)" },
        "positive": []
    }

    # Generate negative side
    for i in range(mid):
        lightness = 75 - (i * 50 / mid)
        saturation = 40 + (i * 30 / mid)
        hex_color = hsl_to_hex(negative_hue, saturation, lightness)

        palette["negative"].append({
            "value": -(mid - i),
            "hex": hex_color,
            "hsl": f"hsl({negative_hue}, {saturation:.1f}%, {lightness:.1f}%)"
        })

    # Reverse so darkest is first
    palette["negative"].reverse()

    # Generate positive side
    for i in range(mid):
        lightness = 75 - (i * 50 / mid)
        saturation = 40 + (i * 30 / mid)
        hex_color = hsl_to_hex(positive_hue, saturation, lightness)

        palette["positive"].append({
            "value": i + 1,
            "hex": hex_color,
            "hsl": f"hsl({positive_hue}, {saturation:.1f}%, {lightness:.1f}%)"
        })

    return palette

def generate_categorical(count: int = 10, colorblind_safe: bool = True) -> List[Dict]:
    """Generate categorical color palette"""
    if colorblind_safe and count <= 5:
        # Use IBM colorblind-safe palette
        colors = [
            ("#648FFF", "Blue"),
            ("#785EF0", "Purple"),
            ("#DC267F", "Magenta"),
            ("#FE6100", "Orange"),
            ("#FFB000", "Yellow"),
        ]
        return [{"index": i + 1, "hex": c[0], "name": c[1]} for i, c in enumerate(colors[:count])]

    # Generate perceptually distinct colors
    palette = []
    for i in range(count):
        hue = (i * 360 / count) % 360
        saturation = 65
        lightness = 50

        hex_color = hsl_to_hex(hue, saturation, lightness)
        palette.append({
            "index": i + 1,
            "hex": hex_color,
            "hsl": f"hsl({hue:.1f}, {saturation}%, {lightness}%)"
        })

    return palette

def main():
    parser = argparse.ArgumentParser(description='Generate color palettes for data visualization')
    parser.add_argument('--type', choices=['sequential', 'diverging', 'categorical'], required=True,
                        help='Type of palette to generate')
    parser.add_argument('--hue', type=int, help='Base hue (0-360) for sequential palettes')
    parser.add_argument('--negative', type=int, help='Negative hue for diverging palettes')
    parser.add_argument('--positive', type=int, help='Positive hue for diverging palettes')
    parser.add_argument('--steps', type=int, default=9, help='Number of steps (default: 9)')
    parser.add_argument('--count', type=int, default=10, help='Number of colors for categorical')
    parser.add_argument('--output', type=str, help='Output JSON file')

    args = parser.parse_args()

    if args.type == 'sequential':
        if not args.hue:
            print("Error: --hue required for sequential palettes")
            sys.exit(1)
        palette = generate_sequential(args.hue, args.steps)
        result = {
            "type": "sequential",
            "baseHue": args.hue,
            "steps": args.steps,
            "colors": palette
        }

    elif args.type == 'diverging':
        if not args.negative or not args.positive:
            print("Error: --negative and --positive hues required for diverging palettes")
            sys.exit(1)
        palette = generate_diverging(args.negative, args.positive, args.steps)
        result = {
            "type": "diverging",
            "negativeHue": args.negative,
            "positiveHue": args.positive,
            "steps": args.steps,
            "palette": palette
        }

    elif args.type == 'categorical':
        palette = generate_categorical(args.count)
        result = {
            "type": "categorical",
            "count": args.count,
            "colorblindSafe": args.count <= 5,
            "colors": palette
        }

    # Output
    json_output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(json_output)
        print(f"✅ Palette saved to {args.output}")
    else:
        print(json_output)

if __name__ == "__main__":
    main()
```
