#!/usr/bin/env python3
"""
Generate Mock Images for Testing

Create placeholder images for testing media components without real assets.

Usage:
    python scripts/generate_mock_images.py --count 10 --output ./test-images
    python scripts/generate_mock_images.py --width 800 --height 600 --count 5
"""

import argparse
import sys
from pathlib import Path

def generate_mock_image(width: int, height: int, index: int, output_dir: Path):
    """Generate a single mock image using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Error: Pillow required")
        print("Install: pip install Pillow")
        sys.exit(1)

    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw gradient-like rectangles
    for i in range(10):
        color = (100 + i * 15, 150 + i * 10, 200)
        draw.rectangle(
            [(0, i * height // 10), (width, (i + 1) * height // 10)],
            fill=color
        )

    # Add text
    text = f"Mock Image {index}\n{width}x{height}"

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill='white', font=font, align='center')

    # Save
    filename = output_dir / f"mock-image-{index}.jpg"
    img.save(filename, 'JPEG', quality=85)

    return filename

def main():
    parser = argparse.ArgumentParser(description="Generate mock images")
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of images to generate"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=800,
        help="Image width in pixels"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="Image height in pixels"
    )
    parser.add_argument(
        "--output",
        default="./mock-images",
        help="Output directory"
    )

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {args.count} mock images ({args.width}x{args.height})...")

    for i in range(1, args.count + 1):
        filename = generate_mock_image(args.width, args.height, i, output_dir)
        print(f"  ✓ Created: {filename}")

    print(f"\n✓ Generated {args.count} images in {output_dir}")
    print(f"  Total size: ~{args.count * 50}KB")

if __name__ == "__main__":
    main()
